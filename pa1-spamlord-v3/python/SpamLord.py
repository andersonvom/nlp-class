import sys
import os
import re
import pprint

### Email Regex ###
words = '([A-Za-z0-9_.+-]){2,}'
at_signs_types = ['\s*@\s*', '\s+\(?at\)?\s+', '\s+where\s+', '\s*&#x40;\s*']
at_signs = '(' + '|'.join(at_signs_types) + ')'
dot_marks_types = ['[;:,.]', '\s+\(?dot\)?\s+', '\s+dt\s+', '\s+dom\s+']
dot_marks = '(' + '|'.join(dot_marks_types) + ')'
username = words
subdomain = '(' + words + dot_marks + ')*'
domain = words + dot_marks + words
email_regex = username + at_signs + subdomain + domain

obf_function = '|'.join(['obfuscate'])
obf1_regex = '(%(quotes)s(%(domain)s)%(quotes)s,\s*%(quotes)s(%(username)s)%(quotes)s)'
params = {'quotes': '[\"\']', 'username': username, 'domain': subdomain + domain}

followed_by_regex = '(%(username)s) \(followed by.*?(%(domain)s)' % {'username': username, 'domain': subdomain + domain}

space_separated_regex = 'email:\s+(%(username)s) at (%(domain)s)' % {'username': '([a-z]+)', 'domain': '([a-z]+\s?)+'}

### Phone Regex ###
sep = '(-|\s+)'
country_code = '(\(?\+[0-9]{1,2}\)?:?'+sep+')?'
area_code = '\(?([0-9]{3})\)?'
prefix = '([0-9]{3})'
suffix = '([0-9]{4})'
end_regex = '($|\s|[^A-Za-z0-9])'
phone_number = country_code + area_code +sep+'?'+ prefix +sep+ suffix + end_regex

""" 
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        for match in re.finditer(email_regex, line, re.IGNORECASE):
            email = match.group(0)
            email = re.sub('(?i)'+at_signs, '@', email)
            email = re.sub('(?i)'+dot_marks, '.', email)
            email = re.sub('-', '', email) # overfitting data, since '-' is a valid email character
            email = re.sub('[-_+=,.!@#$%*()]+$', '', email)
            res.append((name, 'e', email))

        function_regex = obf_function + '\(.*' + obf1_regex
        for match in re.finditer(function_regex % params, line, re.IGNORECASE):
            email = '%(username)s@%(domain)s' % {'username': match.group(9), 'domain': match.group(2)}
            res.append((name, 'e', email))

        for match in re.finditer(followed_by_regex, line, re.IGNORECASE):
          email = '%(username)s@%(domain)s' % {'username': match.group(1), 'domain': match.group(3)}
          res.append((name, 'e', email))

        for match in re.finditer(space_separated_regex, line, re.IGNORECASE):
            sanitized_domain = re.sub('\s+', '.', match.group(3).strip())
            sanitized_domain = re.sub('.dot.', '.', sanitized_domain)
            email = '%(username)s@%(domain)s' % {'username': match.group(1), 'domain': sanitized_domain}
            res.append((name, 'e', email))

        for match in re.finditer(phone_number, line):
            phone = '%(area_code)s-%(prefix)s-%(suffix)s' % { 'area_code': match.group(3), 'prefix': match.group(5), 'suffix': match.group(7) }
            res.append((name, 'p', phone))
    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
