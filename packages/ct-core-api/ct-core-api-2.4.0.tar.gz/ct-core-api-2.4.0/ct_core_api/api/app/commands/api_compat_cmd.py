# =================================
# "Definition" Errors
# =================================
# Example: 'da60e31f102bff4619069e4e2f4b5cc3': ['ProjectDraft']
whitelisted_definition_errors = {
    '63a9eb08366f91f620080ef27f58592d': [
        u'_BidMilestoneValidation'
    ],
    '32df472f187e3d21841266a693dc034a': [
        u'UserFeedback',
        u'UserFeedback:ref',
        u'UserFeedback:summary',
        u'UserFeedback:detail'
    ],
    '1e7f7c7c900c7622642762c32d081f3f': [
        u'TeamProjectBidApprovalPending',
    ],
    'b586d5a3a28b8aa11964683484151eb1': [
        u'BidSelectionApprover',
        u'ProjectApprovalRequest',
    ],
    'ca52d7276b26163878dfcdd97fcd62c5': [
        u'ProjectBidApproval',
    ],
    'de0335597baa485098c50ed6bf4f7bb1': [
        u'_ApprovalRequest',
        u'_BidSelectionApproverRankValidation',
    ],
    '48dd9a10b73470db07df1c710288ae07': [
        u'Bid:approval',
        u'Project:approval-pending',
        u'Project:approval',
    ],
}

# =================================
# "Definition Property" Errors
# =================================
# Example: 'da60e31f102bff4619069e4e2f4b5cc3': [('ProjectDraft', 'cost',)]
whitelisted_definition_property_errors = {
    '4a760b73740139e8736bf99b2504b397': [
        (u'Notification:summary', u'created_at'),
        (u'Notification:summary', u'notification_text'),
        (u'Notification:summary', u'entity_description'),
        (u'Notification:summary', u'viewed_at'),
        (u'Notification:summary', u'notification_type'),
    ],
    '1e7f7c7c900c7622642762c32d081f3f': [
        (u'UserContext', u'project_bid_select_approver'),
        (u'Project:public', u'approval_requests')
    ],
    'b586d5a3a28b8aa11964683484151eb1': [
        (u'Project', u'approval_requests'),
        (u'Project:approval', u'approval_requests'),
        (u'Project:detail', u'approval_requests'),
        (u'Project:public', u'approval_requests'),
        (u'Project:proposal', u'approval_requests'),
        (u'ProjectDraft', u'approval_requests'),
        (u'ApprovalRequest', u'cycle'),
    ],
    'ca52d7276b26163878dfcdd97fcd62c5': [
        (u'Project:approval', u'selected_bid'),
        (u'ProjectDraft', u'bid_approval_requests'),
        (u'Project:public', u'bid_approval_requests'),
        (u'Project:proposal', u'bid_approval_requests'),
        (u'Project', u'bid_approval_requests'),
        (u'Project:detail', u'bid_approval_requests'),
        (u'Project:approval', u'bid_approval_requests'),
    ],
    'de0335597baa485098c50ed6bf4f7bb1': [
        (u'ApprovalRequest', u'status'),
        (u'ApprovalRequest', u'modified_at'),
        (u'ApprovalRequest', u'approver_user'),
        (u'ApprovalRequest', u'rank'),
        (u'ApproverStatus', u'approver_user'),
        (u'Bid:detail', u'selection_approval_requests'),
        (u'BidSelectionApprovalRequest', u'requesting_user'),
    ],
    '48dd9a10b73470db07df1c710288ae07': [
        (u'Bid', u'selection_approval_requests'),
    ],
}

# =================================
# "Path" Errors
# =================================
# Example: 'da60e31f102bff4619069e4e2f4b5cc3': ['/v1.0/project/draft/{id}']
whitelisted_path_errors = {
    '63a9eb08366f91f620080ef27f58592d': [
        u'/v1.0/teams/{team_id}/positions/{position_id}/applications/{id}',
        u'/v1.0/teams/{team_id}/positions/{position_id}/applications',
        u'/v1.0/teams/{team_id}/positions/{position_id}/members/{id}',
        u'/v1.0/teams/{team_id}/positions/{position_id}/members',
        u'/v1.0/teams/{team_id}/positions/{position_id}/applications/{id}',
        u'/v1.0/teams/{team_id}/positions/{position_id}/applications',
        u'/v1.0/teams/{team_id}/positions/{position_id}/members/{id}',
        u'/v1.0/teams/{team_id}/positions/{position_id}/members'
    ],
    'af3d48afc55dcd4c815b4d7b985b0f63': [
        u'/v1.0/teamprojects/{project_id}/{user_id}/feedback/{id}'
    ],
    '1e7f7c7c900c7622642762c32d081f3f': [
        u'/v1.0/team/owner/remove',
    ],
    'b586d5a3a28b8aa11964683484151eb1': [
        u'/v1.0/projects/{project_id}/bid/approval/deny',
        u'/v1.0/projects/{project_id}/bid/approvers',
        u'/v1.0/projects/{project_id}/bid/approval/grant',
        u'/v1.0/user/approver/transactions',
        u'/v1.0/user/approver/transactions/summary',
        u'/v1.0/projects/{project_id}/selected-bid/approval-requests'
    ],
    'ca52d7276b26163878dfcdd97fcd62c5': [
        u'/v1.0/approvals/tiers/bids',
        u'/v1.0/approvals/tiers/projects',
        u'/v1.0/approvals/projects-pending',
    ],
    'de0335597baa485098c50ed6bf4f7bb1': [
        u'/v1.0/projects/{project_id}/bid-selection/approval/deny',
        u'/v1.0/projects/{project_id}/bid-selection/approvers',
        u'/v1.0/projects/{project_id}/bid-selection/approval/grant',
    ],
    '48dd9a10b73470db07df1c710288ae07': [
        u'/v1.0/approver/projects/bid-pending',
        u'/v1.0/approver/projects',
    ],
}

# =================================
# "Path Action" Errors
# =================================
# Example: 'da60e31f102bff4619069e4e2f4b5cc3': [('/v1.0/project/draft/{id}', 'post',)]
whitelisted_path_action_errors = {
    'af3d48afc55dcd4c815b4d7b985b0f63': [(u'/v1.0/teamprojects/{project_id}/users/{user_id}/feedback', u'get',)],
    'b586d5a3a28b8aa11964683484151eb1': [(u'/v1.0/projects/{project_id}/bid-selection/approvers', u'get')],
    'de0335597baa485098c50ed6bf4f7bb1': [
        (u'/v1.0/approver/projects/bid-pending', u'get'),
        (u'/v1.0/bid-selection-approval-requests/{bid_selection_approval_request_id}/deny', u'post'),
        (u'/v1.0/projects/{project_id}/bid-selection-approval-requests', u'get'),
        (u'/v1.0/bids/{bid_id}/bid-selection-approval-requests', u'post'),
        (u'/v1.0/approver/projects', u'get'),
        (u'/v1.0/bid-selection-approval-requests/{bid_selection_approval_request_id}/grant', u'post'),
    ]
}

# =================================
# "Path Action Property" Errors
# =================================
# Example: 'da60e31f102bff4619069e4e2f4b5cc3': [('/v1.0/project/draft/{id}', 'post', 'term_sheet')]
whitelisted_path_action_property_errors = {
    '4a760b73740139e8736bf99b2504b397': [
        (u'/v1.0/user/notifications', u'get'),
        (u'/v1.0/notifications/mark-viewed', u'post')
    ]
}

# =================================
# "Path Action Response" Errors
# =================================
# Example 'da60e31f102bff4619069e4e2f4b5cc3': [('/v1.0/project/draft/{id}', 'post',])
whitelisted_path_action_response_errors = {
    '4a760b73740139e8736bf99b2504b397': [
        (u'/v1.0/user/notifications', u'get'),
        (u'/v1.0/notifications/mark-viewed', u'post')
    ],
    'de0335597baa485098c50ed6bf4f7bb1': [
        (u'/v1.0/approver/projects/bid-pending', u'get'),
        (u'/v1.0/bid-selection-approval-requests/{bid_selection_approval_request_id}/deny', u'post'),
        (u'/v1.0/projects/{project_id}/bid-selection-approval-requests', u'get'),
        (u'/v1.0/bids/{bid_id}/bid-selection-approval-requests', u'post'),
        (u'/v1.0/approver/projects', u'get'),
        (u'/v1.0/bid-selection-approval-requests/{bid_selection_approval_request_id}/grant', u'post'),
    ]
}

WHITELISTED_ERRORS = {
    WHITELIST_DEFINITION_ERRORS: whitelisted_definition_errors,
    WHITELIST_DEFINITION_PROPERTY_ERRORS: whitelisted_definition_property_errors,
    WHITELIST_PATH_ERRORS: whitelisted_path_errors,
    WHITELIST_PATH_ACTION_ERRORS: whitelisted_path_action_errors,
    WHITELIST_PATH_ACTION_PROPERTY_ERRORS: whitelisted_path_action_property_errors,
    WHITELIST_PATH_ACTION_RESPONSE_ERRORS: whitelisted_path_action_response_errors,
}


class APIBackwardsCompatibleVerificationCommand(BaseCommand):
    """
    Command to determine if the API is backwards compatible.
    """

    option_list = [Option('--strict', '-s', dest='strict', action="store_true", default=False)]

    WHITELIST_DEFINITION_ERRORS = 'Definition'
    WHITELIST_DEFINITION_PROPERTY_ERRORS = 'Definition Property'
    WHITELIST_PATH_ERRORS = 'Path'
    WHITELIST_PATH_ACTION_ERRORS = 'Path Action'
    WHITELIST_PATH_ACTION_PROPERTY_ERRORS = 'Path Action Property'
    WHITELIST_PATH_ACTION_RESPONSE_ERRORS = 'Path Action Response'

    def run(self, **kwargs):
        """
        Pull down the latest production swagger.json and compare to the current in code version.
        Prints message, or throws exception with Strict option, if not backwards compatible.
        :return: None
        """
        from hourlynerd.api import hn_api
        from hourlynerd.api.common import json_utils as ju

        strict = kwargs.get('strict', False)

        # Get the swagger.json from production
        resp = requests.get('https://api.hourlynerd.com/swagger.json')
        existing_swagger = ju.loads(resp.text)

        # Really cheap, but make sure to sort "tags" array by description value + name value
        existing_swagger['tags'].sort(key=lambda t: '{0} {1}'.format(t['description'], t['name']))

        existing_md5 = hashlib.md5(ju.dumps(existing_swagger, sort_keys=True)).hexdigest()
        self._set_current_whitelist_for_md5(existing_md5)

        with self.api_app.test_request_context('/'):
            new_swagger = hn_api.swagger_view()().get()

        is_backwards_compatible, messages = self.verify_schemas_are_backwards_compatible(new_swagger, existing_swagger)

        if not is_backwards_compatible:
            error_msg = 'Encountered {0} potentially non backwards compatible API change(s):\n{1}'.format(
                len(messages), '\n'.join(messages))
            print 'MD5: {0}'.format(existing_md5)
            print error_msg
            if strict:
                raise Exception(error_msg)

        return

    def verify_schemas_are_backwards_compatible(self, new_schema, existing_schema):
        """
        Verifies if 2 swagger.json schemas are backwards compatible.
        :param new_schema: JSON loaded swagger.json schema
        :param existing_schema: JSON loaded swagger.json schema
        :return: (is_compatible, msg)
        """

        # Iterate over the path descriptions and see if the are backwards compatible
        is_backwards_compatible, messages = \
            self._verify_api_path_descriptions_are_backwards_compatible(new_schema['paths'], existing_schema['paths'])

        # Iterate over the object definitions
        if is_backwards_compatible:
            is_backwards_compatible, messages = \
                self._verify_api_definitions_are_backwards_compatible(
                    new_schema['definitions'], existing_schema['definitions'])

        return is_backwards_compatible, messages

    def __resolve_dict_with_properties(self, definition):
        if 'allOf' in definition:
            for x in definition['allOf']:
                if 'properties' in x:
                    return x
        elif 'properties' in definition:
            return definition
        else:
            raise Exception('definition does not contain "properties"')

    def __generate_full_error_message(self, err_message, whitelist_entry_type, *whitelist_entry_values):
        entry_value = ', '.join(["{!r}".format(v) for v in whitelist_entry_values])
        if len(whitelist_entry_values) > 1:
            entry_value = "({})".format(entry_value)

        whitelist_entry_message = "\"{}\" whitelist entry:\n\t\t{}".format(whitelist_entry_type, entry_value)

        return '\n\t'.join(["\n{}".format(err_message), whitelist_entry_message])

    def _set_current_whitelist_for_md5(self, md5):
        self._whitelisted_definition_errors = \
            self.WHITELISTED_ERRORS[self.WHITELIST_DEFINITION_ERRORS].get(md5, [])
        self._whitelisted_definition_property_errors = \
            self.WHITELISTED_ERRORS[self.WHITELIST_DEFINITION_PROPERTY_ERRORS].get(md5, [])
        self._whitelisted_path_errors = \
            self.WHITELISTED_ERRORS[self.WHITELIST_PATH_ERRORS].get(md5, [])
        self._whitelisted_path_action_errors = \
            self.WHITELISTED_ERRORS[self.WHITELIST_PATH_ACTION_ERRORS].get(md5, [])
        self._whitelisted_path_action_property_errors = \
            self.WHITELISTED_ERRORS[self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS].get(md5, [])
        self._whitelisted_path_action_response_errors = \
            self.WHITELISTED_ERRORS[self.WHITELIST_PATH_ACTION_RESPONSE_ERRORS].get(md5, [])

    def _verify_api_definitions_are_backwards_compatible(self, new_definitions, existing_definitions):
        """
        Check our API definitions to see if changes are backwards compatible.
        :param new_definitions: { definition_name: { definition_dict } }
        :param existing_definitions: { definition_name: { definition_dict } }
        :return: (is_compatible, msg)
        """
        err_messages = []

        # Ensure we haven't dropped a definition
        for definition_name, definition in existing_definitions.iteritems():

            if definition_name not in new_definitions:
                if definition_name in self._whitelisted_definition_errors:
                    continue

                err_messages.append(self.__generate_full_error_message(
                    'Definition "{0}" missing from latest API'.format(definition_name),
                    self.WHITELIST_DEFINITION_ERRORS,
                    definition_name))
            else:
                is_backwards_compatible, messages = \
                    self._verify_definition_is_backwards_compatible(
                        definition_name, new_definitions[definition_name], definition)

                if not is_backwards_compatible:
                    err_messages.extend(
                        ['\nProblem with definition "{0}": {1}'.format(definition_name, msg) for msg in messages])

        return not err_messages, err_messages

    def _verify_definition_is_backwards_compatible(self, definition_name, new_definition, existing_definition):
        """

        :param new_definition: {dict of definition values - required, properties, etc.}
        :param existing_definition: {dict of definition values - required, properties, etc.}
        :return: (is_compatible, msg)
        """
        err_messages = []

        # Make sure no properties are dropped in the new definition
        for property_name, property_definition in self.__resolve_dict_with_properties(existing_definition)['properties'].iteritems():

            # Skip if we've whitelisted.
            if (definition_name, property_name,) in self._whitelisted_definition_property_errors:
                continue

            if property_name not in new_definition['properties']:
                err_messages.append(self.__generate_full_error_message(
                    'Definition missing property "{0}"'.format(property_name),
                    self.WHITELIST_DEFINITION_PROPERTY_ERRORS,
                    definition_name,
                    property_name))
            else:
                new_property_definition = new_definition['properties'][property_name]

                if '$ref' in property_definition:
                    if '$ref' not in new_property_definition:
                        err_messages.append(self.__generate_full_error_message(
                            'Property no longer has a $ref attribute',
                            self.WHITELIST_DEFINITION_PROPERTY_ERRORS,
                            definition_name,
                            property_name))
                    else:
                        # Ensure the type of the parameter hasn't changed
                        if property_definition['$ref'] != new_property_definition['$ref']:
                            err_messages.append(self.__generate_full_error_message(
                                "Ref \"{0}\" type changed in new definition".format(property_definition['$ref']),
                                self.WHITELIST_DEFINITION_PROPERTY_ERRORS,
                                definition_name,
                                property_name))
                elif 'type' in property_definition:
                    if 'type' not in new_property_definition:
                        err_messages.append(self.__generate_full_error_message(
                            'Property no longer has a type attribute',
                            self.WHITELIST_DEFINITION_PROPERTY_ERRORS,
                            definition_name,
                            property_name))

                    # Ensure the type of the parameter hasn't changed
                    if property_definition['type'] != new_property_definition['type']:
                        err_messages.append(self.__generate_full_error_message(
                            'Property type "{0}" changed in new definition'.format(property_definition['type']),
                            self.WHITELIST_DEFINITION_PROPERTY_ERRORS,
                            definition_name,
                            property_name))

                    # If the parameter is a string, and the parameter has an enum value
                    if property_definition['type'] == 'string' and 'enum' in property_definition:
                        for existing_enum in property_definition['enum']:
                            if existing_enum not in new_property_definition['enum']:
                                err_messages.append(self.__generate_full_error_message(
                                    'Enum "{0}" does not exist in new definition'.format(existing_enum),
                                    self.WHITELIST_DEFINITION_PROPERTY_ERRORS,
                                    definition_name,
                                    property_name))

        return not err_messages, err_messages

    def _verify_api_path_descriptions_are_backwards_compatible(self, new_path_descriptions, existing_path_descriptions):
        """
        :param new_path_descriptions: {path: {action: description}}
        :param existing_path_descriptions: {path: {action: description}}
        :return: (is_compatible, msg)
        """
        err_messages = []

        # Ensure that for each existing API action, there is a corresponding new API action
        for path, path_description in existing_path_descriptions.iteritems():
            if path not in new_path_descriptions:
                # Skip if we've whitelisted.
                if path not in self._whitelisted_path_errors:
                    err_messages.append(self.__generate_full_error_message(
                        'Path "{0}" dropped in new API'.format(path),
                        self.WHITELIST_PATH_ERRORS,
                        path))
            else:
                # Ensure that for each action within a path, it exists in the new version
                for action, existing_action_definition in path_description.iteritems():
                    if action not in new_path_descriptions[path]:
                        # Skip if we've whitelisted.
                        if (path, action,) not in self._whitelisted_path_action_errors:
                            err_messages.append(self.__generate_full_error_message(
                                'Path "{0}" action "{1}" not in new API'.format(path, action),
                                self.WHITELIST_PATH_ACTION_ERRORS,
                                path,
                                action))
                    else:
                        are_path_action_descriptions_compliant, messages = \
                            self._verify_api_path_action_descriptions_are_backwards_compatible(
                                (path, action,),
                                new_path_descriptions[path][action],
                                existing_action_definition)

                        if not are_path_action_descriptions_compliant:
                            err_messages.extend([self.__generate_full_error_message(
                                'Path "{0}" ("{1}"):\n\t{2}'.format(path, action, msg),
                                self.WHITELIST_PATH_ACTION_ERRORS,
                                path,
                                action) for msg in messages])

        return not err_messages, err_messages

    def _verify_api_path_action_descriptions_are_backwards_compatible(
            self, path_action_tuple, new_path_definition, existing_path_definition):
        """
        Given a GET/POST/PATCH/etc... command, ensure the definitions are backwards compatible
        :param new_path_definition: The new definition for the command, the dict
        :param existing_path_definition: The existing definition for the command, the dict
        :return: (is_compatible, msg)
        """

        # Parameter verification:
        # - No parameters dropped
        # - No new parameters set to required
        # - No existing parameters set to required
        # - No type changes on existing parameters
        err_messages = []
        path, action = path_action_tuple

        if 'parameters' in existing_path_definition:
            for existing_parameter in existing_path_definition['parameters']:
                prop = existing_parameter['name']
                path_action_property = (path, action, prop)

                # Skip if we've whitelisted.
                if path_action_property in self._whitelisted_path_action_property_errors:
                    continue

                # Ensure parameter has not been dropped
                if 'parameters' not in new_path_definition:
                    err_messages.append(self.__generate_full_error_message(
                        'No parameters in new definition',
                        self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS,
                        *path_action_property))

                new_parameter = next((p for p in new_path_definition['parameters']
                                      if p['name'] == prop), None)

                if new_parameter is None:
                    err_messages.append(self.__generate_full_error_message(
                        'Parameter "{0}" dropped in new definition'.format(prop),
                        self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS,
                        *path_action_property))
                else:
                    # Ensure if old parameter is not required, new parameter is not required as well.
                    if (not existing_parameter.get('required', False)) and new_parameter.get('required', False):
                        err_messages.append(self.__generate_full_error_message(
                            'Parameter "{0}" marked required in new definition'.format(prop),
                            self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS,
                            *path_action_property))

                    # Ensure the type of the parameter hasn't changed
                    if existing_parameter['type'] != new_parameter['type']:
                        err_messages.append(self.__generate_full_error_message(
                            'Parameter "{0}" type changed in new definition'.format(prop),
                            self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS,
                            *path_action_property))

                    # If the parameter is a string, and the parameter has an enum value
                    if existing_parameter['type'] == 'string' and 'enum' in existing_parameter:
                        for existing_enum in existing_parameter['enum']:
                            if existing_enum not in new_parameter['enum']:
                                err_messages.append(self.__generate_full_error_message(
                                    'Enum "{0}" does not exist in new definition'.format(existing_enum),
                                    self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS,
                                    *path_action_property))

                    # Ensure the location of the parameter hasn't changed
                    if existing_parameter['in'] != new_parameter['in']:
                        err_messages.append(self.__generate_full_error_message(
                            'Parameter "{0}" type changed location in new definition'.format(prop),
                            self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS,
                            *path_action_property))

        # Get the list of new parameters
        existing_parameter_names = [ep['name'] for ep in existing_path_definition.get('parameters', [])]
        new_parameters = [p for p in new_path_definition.get('parameters', []) if p['name'] not in existing_parameter_names]

        # Ensure that new parameters aren't set to required.
        for np in new_parameters:
            path_action_property = (path_action_tuple[0], path_action_tuple[1], np['name'])

            # Skip if we've whitelisted.
            if path_action_property in self._whitelisted_path_action_property_errors:
                continue

            if np.get('required', False):
                err_messages.append(self.__generate_full_error_message(
                    'New parameter "{0}" set to required'.format(np['name']),
                    self.WHITELIST_PATH_ACTION_PROPERTY_ERRORS,
                    *path_action_property))

        # Responses
        # Ensure that if we have a 200 response the underlying schema is the same.
        if '200' in existing_path_definition['responses']:
            existing_schema = existing_path_definition['responses']['200'].get('schema')
            new_schema = new_path_definition['responses']['200'].get('schema')
            if existing_schema != new_schema:
                # Skip if we've whitelisted.
                if path_action_tuple not in self._whitelisted_path_action_response_errors:
                    err_messages.append(self.__generate_full_error_message(
                        'New response contains different schema {0}'.format(new_schema),
                        self.WHITELIST_PATH_ACTION_RESPONSE_ERRORS,
                        *path_action_tuple))

        return not err_messages, err_messages
