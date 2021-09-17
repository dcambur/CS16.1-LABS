import re


class AuditParser:
    def __init__(self, audit_file):
        self.audit_file = open(audit_file, 'r').readlines()

    def _element_list(self):
        element_list = []
        check_element_regex = re.compile(r'^[\s](.+?):.+')  # search key : value pairs
        for line in self.audit_file:
            check_element = check_element_regex.match(line)
            if check_element:
                element = check_element.group(1).lstrip()
                element = element.rstrip()
                # remove element contains '<'
                if not re.search(r'<', element):
                    if element not in element_list:
                        element_list.append(element)
        # new element for reference. it takes value from 'description'
        element_list.append('ref')
        return element_list

    def array(self):
        """this return list of dictionary contain all element"""

        start_flag = None
        # temporary dict to store element
        temp_datastore = {}
        array = []
        # use to capture 'element : value'
        master_regex = re.compile(r'^[\s](.+?):(.+)')
        element_list = self._element_list()
        for line in self.audit_file:
            # set the flag to start enumerate elemet under </custom_item>
            if re.match(r'.+(<custom_item).+', line):
                start_flag = 1
                # if found line with </custom_item> reset the flag and start
            # to store item in tempDatastore into actual array
            if re.match(r'.+(</custom_item).+', line):
                start_flag = 0
                # fill empty element with value n/a
                for element in element_list:
                    if element not in temp_datastore:
                        temp_datastore[element] = "n/a"
                array.append(temp_datastore)
                temp_datastore = {}  # reset datastore
            # START
            # start to collect the elements
            if start_flag == 1:
                match_line = master_regex.match(line)
                if match_line:
                    # traverse all element found in audit file
                    for element in element_list:
                        if match_line.group(1).lstrip().rstrip() == element:
                            value = match_line.group(2).lstrip().rstrip()
                            # remove " from value
                            value = value.lstrip("\"")
                            value = value.rstrip("\"")
                            # for description contain numbering, we split it
                            if element == 'description':
                                # split number and real description
                                if re.match(r'^(\d)', value):
                                    ref = value.split(" ", 1)
                                    temp_datastore[element] = ref[1]
                                    # store the number in its keys
                                    temp_datastore["ref"] = ref[0]
                                # if description contains no numbering, just
                                # push to temp datastore
                                else:
                                    temp_datastore[element] = value
                            else:
                                temp_datastore[element] = value
        return array
