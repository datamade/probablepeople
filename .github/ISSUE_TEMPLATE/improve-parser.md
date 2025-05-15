---
name: Improve Parser
about: Is a parse not looking the way you expected? Let us know here!
title: ''
labels: bad parse
assignees: ''

---

**The Input Name**
What string are you having an issue with?

(ex. Mr George 'Gob' Bluth II)

**Current Output**
What is the parser currently returning?

Mr - GivenName
George - GivenName
'Gob' - Nickname
Bluth - Surname
II - Surname

**Expected Ouput**
What are you expecting the parser to return?

Mr - PrefixMarital
George - GivenName
'Gob' - Nickname
Bluth - Surname
II - SuffixGenerational

**Examples**
Preferably 8-12 real world examples with a similar pattern that we can use to train the parser. This can be from your dataset if you're comfortable sharing some.
- Ms Deborah 'DJ' Vance Jr

**Additional context**
Optional. Add any other context here.
