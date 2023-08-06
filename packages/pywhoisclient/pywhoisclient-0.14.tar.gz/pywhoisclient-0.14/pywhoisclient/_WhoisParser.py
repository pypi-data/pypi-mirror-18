

class WhoisParser(object):
    def parse(self, raw_data):
        result = []
        #
        for line in [x.strip() for x in raw_data.splitlines()]:
            # Step 1. Skip comment
            if line.startswith('%'):
                continue
            # Step 2. Parse value
            if ":" in line:
                name, value = line.split(':', 1)
                name = name.strip()
                value = value.strip()
                result.append((name, value))
        #
        return result
