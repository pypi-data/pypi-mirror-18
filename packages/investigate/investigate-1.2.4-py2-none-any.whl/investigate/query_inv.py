#!/usr/bin/env python

import investigate


inv = investigate.Investigate('9eb8e4a5-083f-4c83-8428-53302e702681')
result = inv.prefixes_for_asn(36692)

print result

#print "EOF"

