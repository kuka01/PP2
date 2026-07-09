# Python Regular Expressions

## search()

```python
import re

text = "Python is fun"

x = re.search("Python", text)

print(x)
```

---

## findall()

```python
import re

text = "cat dog cat bird"

print(re.findall("cat", text))
```

---

## split()

```python
import re

text = "apple,banana,orange"

print(re.split(",", text))
```

---

## sub()

```python
import re

text = "I like cats"

print(re.sub("cats", "dogs", text))
```

---

## match()

```python
import re

text = "Python"

print(re.match("Py", text))
```

---

## Metacharacters

```
.
^
$
*
+
?
{}
[]
|
()
```

---

## Special Sequences

```
\d
\D
\s
\S
\w
\W
\A
\Z
```

---

## Quantifiers

```
*
+
?
{2}
{2,4}
```