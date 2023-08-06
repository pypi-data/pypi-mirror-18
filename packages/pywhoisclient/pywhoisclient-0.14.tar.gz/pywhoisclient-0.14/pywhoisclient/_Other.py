    def other(self):
                # Whois.com is a bit special... Fabulous.com also seems to use this format. As do some others.
                match = re.search("^\s?Name\s?[Ss]ervers:?\s*\n((?:\s*.+\n)+?\s?)\n", segment, re.MULTILINE)
                if match is not None:
                        chunk = match.group(1)
                        for match in re.findall("[ ]*(.+)\n", chunk):
                                if match.strip() != "":
                                        if not re.match("^[a-zA-Z]+:", match):
                                                try:
                                                        data["nameservers"].append(match.strip())
                                                except KeyError as e:
                                                        data["nameservers"] = [match.strip()]
                # Nominet also needs some special attention
                match = re.search("    Registrar:\n        (.+)\n", segment)
                if match is not None:
                        data["registrar"] = [match.group(1).strip()]
                match = re.search("    Registration status:\n        (.+)\n", segment)
                if match is not None:
                        data["status"] = [match.group(1).strip()]
                match = re.search("    Name servers:\n([\s\S]*?\n)\n", segment)
                if match is not None:
                        chunk = match.group(1)
                        for match in re.findall("        (.+)\n", chunk):
                                match = match.split()[0]
                                try:
                                        data["nameservers"].append(match.strip())
                                except KeyError as e:
                                        data["nameservers"] = [match.strip()]
                # janet (.ac.uk) is kinda like Nominet, but also kinda not
                match = re.search("Registered By:\n\t(.+)\n", segment)
                if match is not None:
                        data["registrar"] = [match.group(1).strip()]
                match = re.search("Entry created:\n\t(.+)\n", segment)
                if match is not None:
                        data["creation_date"] = [match.group(1).strip()]
                match = re.search("Renewal date:\n\t(.+)\n", segment)
                if match is not None:
                        data["expiration_date"] = [match.group(1).strip()]
                match = re.search("Entry updated:\n\t(.+)\n", segment)
                if match is not None:
                        data["updated_date"] = [match.group(1).strip()]
                match = re.search("Servers:([\s\S]*?\n)\n", segment)
                if match is not None:
                        chunk = match.group(1)
                        for match in re.findall("\t(.+)\n", chunk):
                                match = match.split()[0]
                                try:
                                        data["nameservers"].append(match.strip())
                                except KeyError as e:
                                        data["nameservers"] = [match.strip()]
                # .am plays the same game
                match = re.search("   DNS servers:([\s\S]*?\n)\n", segment)
                if match is not None:
                        chunk = match.group(1)
                        for match in re.findall("      (.+)\n", chunk):
                                match = match.split()[0]
                                try:
                                        data["nameservers"].append(match.strip())
                                except KeyError as e:
                                        data["nameservers"] = [match.strip()]
                # SIDN isn't very standard either. And EURid uses a similar format.
                match = re.search("Registrar:\n\s+(?:Name:\s*)?(\S.*)", segment)
                if match is not None:
                        data["registrar"].insert(0, match.group(1).strip())
                match = re.search("(?:Domain nameservers|Name servers):([\s\S]*?\n)\n", segment)
                if match is not None:
                        chunk = match.group(1)
                        for match in re.findall("\s+?(.+)\n", chunk):
                                match = match.split()[0]
                                # Prevent nameserver aliases from being picked up.
                                if not match.startswith("[") and not match.endswith("]"):
                                        try:
                                                data["nameservers"].append(match.strip())
                                        except KeyError as e:
                                                data["nameservers"] = [match.strip()]
                # The .ie WHOIS server puts ambiguous status information in an unhelpful order
                match = re.search('ren-status:\s*(.+)', segment)
                if match is not None:
                        data["status"].insert(0, match.group(1).strip())
                # nic.it gives us the registrar in a multi-line format...
                match = re.search('Registrar\n  Organization:     (.+)\n', segment)
                if match is not None:
                        data["registrar"] = [match.group(1).strip()]
                # HKDNR (.hk) provides a weird nameserver format with too much whitespace
                match = re.search("Name Servers Information:\n\n([\s\S]*?\n)\n", segment)
                if match is not None:
                        chunk = match.group(1)
                        for match in re.findall("(.+)\n", chunk):
                                match = match.split()[0]
                                try:
                                        data["nameservers"].append(match.strip())
                                except KeyError as e:
                                        data["nameservers"] = [match.strip()]
                # ... and again for TWNIC.
                match = re.search("   Domain servers in listed order:\n([\s\S]*?\n)\n", segment)
                if match is not None:
                        chunk = match.group(1)
                        for match in re.findall("      (.+)\n", chunk):
                                match = match.split()[0]
                                try:
                                        data["nameservers"].append(match.strip())
                                except KeyError as e:
                                        data["nameservers"] = [match.strip()]
                

        data["contacts"] = parse_registrants(raw_data, never_query_handles, handle_server)

        # Parse dates
        try:
                data['expiration_date'] = remove_duplicates(data['expiration_date'])
                data['expiration_date'] = parse_dates(data['expiration_date'])
        except KeyError as e:
                pass # Not present

        try:
                data['creation_date'] = remove_duplicates(data['creation_date'])
                data['creation_date'] = parse_dates(data['creation_date'])
        except KeyError as e:
                pass # Not present

        try:
                data['updated_date'] = remove_duplicates(data['updated_date'])
                data['updated_date'] = parse_dates(data['updated_date'])
        except KeyError as e:
                pass # Not present

        try:
                data['nameservers'] = remove_suffixes(data['nameservers'])
                data['nameservers'] = remove_duplicates([ns.rstrip(".") for ns in data['nameservers']])
        except KeyError as e:
                pass # Not present

        try:
                data['emails'] = remove_duplicates(data['emails'])
        except KeyError as e:
                pass # Not present

        try:
                data['registrar'] = remove_duplicates(data['registrar'])
        except KeyError as e:
                pass # Not present

        # Remove e-mail addresses if they are already listed for any of the contacts
        known_emails = []
        for contact in ("registrant", "tech", "admin", "billing"):
                if data["contacts"][contact] is not None:
                        try:
                                known_emails.append(data["contacts"][contact]["email"])
                        except KeyError as e:
                                pass # No e-mail recorded for this contact...
        try:
                data['emails'] = [email for email in data["emails"] if email not in known_emails]
        except KeyError as e:
                pass # Not present

        for key in list(data.keys()):
                if data[key] is None or len(data[key]) == 0:
                        del data[key]

        data["raw"] = raw_data

        if normalized != []:
                data = normalize_data(data, normalized)

        return data

    def normalize_data(data, normalized):
        for key in ("nameservers", "emails", "whois_server"):
                if key in data and data[key] is not None and (normalized == True or key in normalized):
                        if is_string(data[key]):
                                data[key] = data[key].lower()
                        else:
                                data[key] = [item.lower() for item in data[key]]

        for key, threshold in (("registrar", 4), ("status", 3)):
                if key == "registrar":
                        ignore_nic = True
                else:
                        ignore_nic = False
                if key in data and data[key] is not None and (normalized == True or key in normalized):
                        if is_string(data[key]):
                                data[key] = normalize_name(data[key], abbreviation_threshold=threshold, length_threshold=1, ignore_nic=ignore_nic)
                        else:
                                data[key] = [normalize_name(item, abbreviation_threshold=threshold, length_threshold=1, ignore_nic=ignore_nic) for item in data[key]]

        for contact_type, contact in data['contacts'].items():
                if contact is not None:
                        if 'country' in contact and contact['country'] in countries:
                                contact['country'] = countries[contact['country']]
                        if 'city' in contact and contact['city'] in airports:
                                contact['city'] = airports[contact['city']]
                        if 'country' in contact and 'state' in contact:
                                for country, source in (("united states", states_us), ("australia", states_au), ("canada", states_ca)):
                                        if country in contact["country"].lower() and contact["state"] in source:
                                                contact["state"] = source[contact["state"]]
                        
                        for key in ("email",):
                                if key in contact and contact[key] is not None and (normalized == True or key in normalized):
                                        if is_string(contact[key]):
                                                contact[key] = contact[key].lower()
                                        else:
                                                contact[key] = [item.lower() for item in contact[key]]

                        for key in ("name", "street"):
                                if key in contact and contact[key] is not None and (normalized == True or key in normalized):
                                        contact[key] = normalize_name(contact[key], abbreviation_threshold=3)

                        for key in ("city", "organization", "state", "country"):
                                if key in contact and contact[key] is not None and (normalized == True or key in normalized):
                                        contact[key] = normalize_name(contact[key], abbreviation_threshold=3, length_threshold=3)
                        
                        if "name" in contact and "organization" not in contact:
                                lines = [x.strip() for x in contact["name"].splitlines()]
                                new_lines = []
                                for i, line in enumerate(lines):
                                        for regex in organization_regexes:
                                                if re.search(regex, line):
                                                        new_lines.append(line)
                                                        del lines[i]
                                                        break
                                if len(lines) > 0:
                                        contact["name"] = "\n".join(lines)
                                else:
                                        del contact["name"]
                                        
                                if len(new_lines) > 0:
                                        contact["organization"] = "\n".join(new_lines)
                                                
                        if "street" in contact and "organization" not in contact:
                                lines = [x.strip() for x in contact["street"].splitlines()]
                                if len(lines) > 1:
                                        for regex in organization_regexes:
                                                if re.search(regex, lines[0]):
                                                        contact["organization"] = lines[0]
                                                        contact["street"] = "\n".join(lines[1:])
                                                        break
                        
                        for key in list(contact.keys()):
                                try:
                                        contact[key] = contact[key].strip(", ")
                                        if contact[key] == "-" or contact[key].lower() == "n/a":
                                                del contact[key]
                                except AttributeError as e:
                                        pass # Not a string
        return data

    def normalize_name(value, abbreviation_threshold=4, length_threshold=8, lowercase_domains=True, ignore_nic=False):
        normalized_lines = []
        for line in value.split("\n"):
                line = line.strip(",") # Get rid of useless comma's
                if (line.isupper() or line.islower()) and len(line) >= length_threshold:
                        # This line is likely not capitalized properly
                        if ignore_nic == True and "nic" in line.lower():
                                # This is a registrar name containing 'NIC' - it should probably be all-uppercase.
                                line = line.upper()
                        else:
                                words = line.split()
                                normalized_words = []
                                if len(words) >= 1:
                                        # First word
                                        if len(words[0]) >= abbreviation_threshold and "." not in words[0]:
                                                normalized_words.append(words[0].capitalize())
                                        elif lowercase_domains and "." in words[0] and not words[0].endswith(".") and not words[0].startswith("."):
                                                normalized_words.append(words[0].lower())
                                        else:
                                                # Probably an abbreviation or domain, leave it alone
                                                normalized_words.append(words[0])
                                if len(words) >= 3:
                                        # Words between the first and last
                                        for word in words[1:-1]:
                                                if len(word) >= abbreviation_threshold and "." not in word:
                                                        normalized_words.append(word.capitalize())
                                                elif lowercase_domains and "." in word and not word.endswith(".") and not word.startswith("."):
                                                        normalized_words.append(word.lower())
                                                else:
                                                        # Probably an abbreviation or domain, leave it alone
                                                        normalized_words.append(word)
                                if len(words) >= 2:
                                        # Last word
                                        if len(words[-1]) >= abbreviation_threshold and "." not in words[-1]:
                                                normalized_words.append(words[-1].capitalize())
                                        elif lowercase_domains and "." in words[-1] and not words[-1].endswith(".") and not words[-1].startswith("."):
                                                normalized_words.append(words[-1].lower())
                                        else:
                                                # Probably an abbreviation or domain, leave it alone
                                                normalized_words.append(words[-1])
                                line = " ".join(normalized_words)
                normalized_lines.append(line)
        return "\n".join(normalized_lines)

    def _parse_dates(self, values):
        parsed_dates = []
        for date in dates:
                for rule in grammar['_dateformats']:
                        result = re.match(rule, date)

                        if result is not None:
                                try:
                                        # These are always numeric. If they fail, there is no valid date present.
                                        year = int(result.group("year"))
                                        day = int(result.group("day"))

                                        # Detect and correct shorthand year notation
                                        if year < 60:
                                                year += 2000
                                        elif year < 100:
                                                year += 1900

                                        # This will require some more guesswork - some WHOIS servers present the name of the month
                                        try:
                                                month = int(result.group("month"))
                                        except ValueError as e:
                                                # Apparently not a number. Look up the corresponding number.
                                                try:
                                                        month = grammar['_months'][result.group("month").lower()]
                                                except KeyError as e:
                                                        # Unknown month name, default to 0
                                                        month = 0

                                        try:
                                                hour = int(result.group("hour"))
                                        except IndexError as e:
                                                hour = 0
                                        except TypeError as e:
                                                hour = 0

                                        try:
                                                minute = int(result.group("minute"))
                                        except IndexError as e:
                                                minute = 0
                                        except TypeError as e:
                                                minute = 0

                                        try:
                                                second = int(result.group("second"))
                                        except IndexError as e:
                                                second = 0
                                        except TypeError as e:
                                                second = 0

                                        break
                                except ValueError as e:
                                        # Something went horribly wrong, maybe there is no valid date present?
                                        year = 0
                                        month = 0
                                        day = 0
                                        hour = 0
                                        minute = 0
                                        second = 0
                                        print(e.message) # FIXME: This should have proper logging of some sort...?
                try:
                        if year > 0:
                                try:
                                        parsed_dates.append(datetime.datetime(year, month, day, hour, minute, second))
                                except ValueError as e:
                                        # We might have gotten the day and month the wrong way around, let's try it the other way around
                                        # If you're not using an ISO-standard date format, you're an evil registrar!
                                        parsed_dates.append(datetime.datetime(year, day, month, hour, minute, second))
                except UnboundLocalError as e:
                        pass

        if len(parsed_dates) > 0:
                return parsed_dates
        else:
                return None

    def remove_duplicates(data):
        cleaned_list = []

        for entry in data:
                if entry not in cleaned_list:
                        cleaned_list.append(entry)

        return cleaned_list

    def remove_suffixes(data):
        # Removes everything before and after the first non-whitespace continuous string.
        # Used to get rid of IP suffixes for nameservers.
        cleaned_list = []
        
        for entry in data:
                cleaned_list.append(re.search("([^\s]+)\s*[\s]*", entry).group(1).lstrip())
                
        return cleaned_list

    def parse_registrants(data, never_query_handles=True, handle_server=""):
        registrant = None
        tech_contact = None
        billing_contact = None
        admin_contact = None

        for segment in data:
                for regex in registrant_regexes:
                        match = re.search(regex, segment)
                        if match is not None:
                                registrant = match.groupdict()
                                break

        for segment in data:
                for regex in tech_contact_regexes:
                        match = re.search(regex, segment)
                        if match is not None:
                                tech_contact = match.groupdict()
                                break

        for segment in data:
                for regex in admin_contact_regexes:
                        match = re.search(regex, segment)
                        if match is not None:
                                admin_contact = match.groupdict()
                                break

        for segment in data:
                for regex in billing_contact_regexes:
                        match = re.search(regex, segment)
                        if match is not None:
                                billing_contact = match.groupdict()
                                break

        # Find NIC handle contact definitions
        handle_contacts = parse_nic_contact(data)

        # Find NIC handle references and process them
        missing_handle_contacts = []
        for category in nic_contact_references:
                for regex in nic_contact_references[category]:
                        for segment in data:
                                match = re.search(regex, segment)
                                if match is not None:
                                        data_reference = match.groupdict()
                                        if data_reference["handle"] == "-" or re.match("https?:\/\/", data_reference["handle"]) is not None:
                                                pass  # Reference was either blank or a URL; the latter is to deal with false positives for nic.ru
                                        else:
                                                found = False
                                                for contact in handle_contacts:
                                                        if contact["handle"] == data_reference["handle"]:
                                                                found = True
                                                                data_reference.update(contact)
                                                if found == False:
                                                        # The contact definition was not found in the supplied raw WHOIS data. If the
                                                        # method has been called with never_query_handles=False, we can use the supplied
                                                        # WHOIS server for looking up the handle information separately.
                                                        if never_query_handles == False:
                                                                try:
                                                                        contact = fetch_nic_contact(data_reference["handle"], handle_server)
                                                                        data_reference.update(contact)
                                                                except WhoisException as e:
                                                                        pass # No data found. TODO: Log error?
                                                        else:
                                                                pass # TODO: Log warning?
                                                if category == "registrant":
                                                        registrant = data_reference
                                                elif category == "tech":
                                                        tech_contact = data_reference
                                                elif category == "billing":
                                                        billing_contact = data_reference
                                                elif category == "admin":
                                                        admin_contact = data_reference
                                        break
                                        
        # Post-processing
        for obj in (registrant, tech_contact, billing_contact, admin_contact):
                if obj is not None:
                        for key in list(obj.keys()):
                                if obj[key] is None or obj[key].strip() == "": # Just chomp all surrounding whitespace
                                        del obj[key]
                                else:
                                        obj[key] = obj[key].strip()
                        if "phone_ext" in obj:
                                if "phone" in obj:
                                        obj["phone"] += " ext. %s" % obj["phone_ext"]
                                        del obj["phone_ext"]
                        if "street1" in obj:
                                street_items = []
                                i = 1
                                while True:
                                        try:
                                                street_items.append(obj["street%d" % i])
                                                del obj["street%d" % i]
                                        except KeyError as e:
                                                break
                                        i += 1
                                obj["street"] = "\n".join(street_items)
                        if "organization1" in obj: # This is to deal with eg. HKDNR, who allow organization names in multiple languages.
                                organization_items = []
                                i = 1
                                while True:
                                        try:
                                                if obj["organization%d" % i].strip() != "":
                                                        organization_items.append(obj["organization%d" % i])
                                                        del obj["organization%d" % i]
                                        except KeyError as e:
                                                break
                                        i += 1
                                obj["organization"] = "\n".join(organization_items)
                        if 'changedate' in obj:
                                obj['changedate'] = parse_dates([obj['changedate']])[0]
                        if 'creationdate' in obj:
                                obj['creationdate'] = parse_dates([obj['creationdate']])[0]
                        if 'street' in obj and "\n" in obj["street"] and 'postalcode' not in obj:
                                # Deal with certain mad WHOIS servers that don't properly delimit address data... (yes, AFNIC, looking at you)
                                lines = [x.strip() for x in obj["street"].splitlines()]
                                if " " in lines[-1]:
                                        postal_code, city = lines[-1].split(" ", 1)
                                        if "." not in lines[-1] and re.match("[0-9]", postal_code) and len(postal_code) >= 3:
                                                obj["postalcode"] = postal_code
                                                obj["city"] = city
                                                obj["street"] = "\n".join(lines[:-1])
                        if 'firstname' in obj or 'lastname' in obj:
                                elements = []
                                if 'firstname' in obj:
                                        elements.append(obj["firstname"])
                                if 'lastname' in obj:
                                        elements.append(obj["lastname"])
                                obj["name"] = " ".join(elements)
                        if 'country' in obj and 'city' in obj and (re.match("^R\.?O\.?C\.?$", obj["country"], re.IGNORECASE) or obj["country"].lower() == "republic of china") and obj["city"].lower() == "taiwan":
                                # There's an edge case where some registrants append ", Republic of China" after "Taiwan", and this is mis-parsed
                                # as Taiwan being the city. This is meant to correct that.
                                obj["country"] = "%s, %s" % (obj["city"], obj["country"])
                                lines = [x.strip() for x in obj["street"].splitlines()]
                                obj["city"] = lines[-1]
                                obj["street"] = "\n".join(lines[:-1])

        return {
                "registrant": registrant,
                "tech": tech_contact,
                "admin": admin_contact,
                "billing": billing_contact,
        }

    def fetch_nic_contact(self, handle, lookup_server):
        response = get_whois_raw(handle, lookup_server)
        response = [segment.replace("\r", "") for segment in response] # Carriage returns are the devil
        results = parse_nic_contact(response)
        
        if len(results) > 0:
                return results[0]
        else:
                raise WhoisException("No contact data found in the response.")
        
    def parse_nic_contact(self, data):
        handle_contacts = []
        for regex in nic_contact_regexes:
                for segment in data:
                        matches = re.finditer(regex, segment)
                        for match in matches:
                                handle_contacts.append(match.groupdict())
                                
        return handle_contacts
