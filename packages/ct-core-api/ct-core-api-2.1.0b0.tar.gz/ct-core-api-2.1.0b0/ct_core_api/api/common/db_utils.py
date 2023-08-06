import logging
from pprint import pprint

from sqlalchemy import inspect

from ct_core_api.api.common import model_selectors
from ct_core_api.common import db_utils as dbu, object_utils as ou

_logger = logging.getLogger(__name__)


########################################
# Performance Helpers
########################################

def optimize_query(q, field_selectors):
    """Produce a new query having an "optimized" loading strategy.
    The loading strategy will restrict the select clauses to only those fields identified by the field selectors.
    A best effort is made to join all relational data but in some cases a subquery loading strategy may be necessary.
    """

    # The column descriptions provide metadata about what will be returned by this query
    col_descriptions = inspect(q).column_descriptions

    # We'll only attempt to optimize a query that has a single top-level model being selected
    if len(col_descriptions) > 1:
        _logger.warn('Unable to optimize query')
        return q

    # The value for 'type' identifies the model class
    model_cls = col_descriptions[0]['type']

    # Identify which model fields and sub-fields correspond to the field selectors
    model_field_selectors = model_selectors.ModelFieldSelectors.from_field_selectors(model_cls, field_selectors)

    try:
        loader_options = model_field_selectors.generate_loader_options()
        return q.options(*loader_options)
    except Exception as exc:
        _logger.warning('Unable to optimize query. Could not generate loader options.', exc_info=exc)
        return q


def evaluate_query_optimization(session, q, schema, limit=None):
    """Tool comparing db performance of a query against its "optimized" version.
    Useful for evaluating whether the `optimize_query` function can be effectively used to speed up serialization.

    The query result(s) will be serialized using the provided schema. All queries issued to the db during the course of
    these operations are recorded and summaries of their performance are printed. If the serialization results aren't
    the same, a textual difference is presented.

    :param q: The SQLAlchemy Query to test. The Query must have a select clause that corresponds to a single `Model`.
    :param schema: The `APISchema` instance that will handle serialization.
    :param limit: The number of items to fetch from the db or None if all results should be fetched.
    """
    def execute_query(q, limit=None):
        if limit is None:
            return q.all()
        elif limit == 1:
            return q.first()
        return q.limit(limit).all()

    def fetch_and_serialize(q, schema):
        session.expunge_all()
        dbu.clear_debug_queries()
        q_result = execute_query(q, limit)
        many = True if hasattr(q_result, '__iter__') else False
        dump_result = schema.dump(q_result, many=many).data
        debug_queries = dbu.get_debug_queries()
        return dump_result, debug_queries

    def print_summary_msg(*msgs):
        print()
        print('*' * 100)
        for msg in msgs:
            print(msg)
        print('*' * 100)

    def print_results_summary(dump_result, debug_queries, label=None):
        label = "Original" if label is None else label
        print_summary_msg("{} query summary:".format(label))
        print(dbu.get_debug_queries_summary(
            debug_queries=debug_queries, collapse_whitespace=False, collapse_select_clauses=False))
        print_summary_msg("{} serialization results:".format(label))
        pprint(dump_result)

    q_a = q
    q_b = optimize_query(q, schema.resolve_field_selectors())

    if q_a == q_b:
        print('Sorry, query could not be optimized!')
        print_results_summary(*fetch_and_serialize(q, schema))
    else:
        dump_result_a, debug_queries_a = fetch_and_serialize(q_a, schema)
        dump_result_b, debug_queries_b = fetch_and_serialize(q_b, schema)

        num_results_a = len(dump_result_a) if isinstance(dump_result_a, list) else 1
        num_results_b = len(dump_result_b) if isinstance(dump_result_b, list) else 1

        num_queries_a = len(debug_queries_a)
        num_queries_b = len(debug_queries_b)
        num_queries_delta = abs(num_queries_b - num_queries_a)

        total_duration_a = sum(dq.duration for dq in debug_queries_a)
        total_duration_b = sum(dq.duration for dq in debug_queries_b)
        total_duration_delta = abs(total_duration_b - total_duration_a)

        advice = []

        if dump_result_a == dump_result_b:
            if num_queries_b <= num_queries_a and total_duration_b <= total_duration_a:
                advice.append("* Use the \"optimized\" version! It runs {} fewer queries and is {} faster!".format(
                    num_queries_delta, total_duration_delta))
            elif num_queries_b <= num_queries_a:
                advice.append("* The \"optimized\" version runs {} fewer queries, but is {} slower.".format(
                    num_queries_delta, total_duration_delta))
            else:
                advice.append(
                    "* Don't use the \"optimized\" version. "
                    "It runs {} more queries and is {} slower.".format(num_queries_delta, total_duration_delta))

            if num_queries_b > num_queries_a:
                advice.append(
                    "* The \"optimized\" query ran {} more queries than the original. "
                    "Try defining `backing_attrs` on the schema's fields to aid the optimizer.".format(
                        num_queries_delta))
        else:
            advice.extend([
                '* Dump results differ! '
                'Don\'t use the "optimized" query, it produced a different serialization result:',
                '',
                ou.get_obj_comparison_message(dump_result_a, dump_result_b)])

        print_results_summary(dump_result_a, debug_queries_a, label='Original')
        print_results_summary(dump_result_b, debug_queries_b, label='Optimized')

        print_summary_msg(
            "Original:  Num queries: {:>2}, Num queries per result: {} Total query duration: {}".format(
                num_queries_a, num_queries_a / float(num_results_a), total_duration_a),
            "Optimized: Num queries: {:>2}, Num queries per result: {} Total query duration: {}".format(
                num_queries_b, num_queries_b / float(num_results_b), total_duration_b))

        print_summary_msg('Advice:', '-' * 80, *advice)
