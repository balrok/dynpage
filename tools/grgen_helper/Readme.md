# Modelparser

Is very stupid regex based.
It can happen that a whitespace or special character produces wrong results
If grgen was defined in antlr4 we could use their parser .. but it is not


Notees to package definitions

Following is not possible:
```
package X {
    node A;
    node B;
}
node C;
```

but you can write something like this
```
node C;
package X {
    node A;
    node B;
}
```

and even this:
```
package X {
    node A;
    node B;
}
package Y {
    node A;
    node B;
}
```
