# PyGen

Gr*Gen* with *Py*thon


idea was to add an alternative implementation to parse grgen and print models and grsi files

especially printing would be great as grsi files are too verbose and hard to script
My goal is to have this:

pn = PetriNet("Test")
p2 = pn.add(Page("Page 2"))

p_s=pn.add(Place("Start", 1)) # added to a default page
p_n=pn.add(Place("Next"))
p_a=pn.add(Place("After"))

t_1=pn.add(Transition("t1"))
t_2=pn.add(Transition("t2"))

Edge(p_s, t_1)
Edge(t_1, p_a)
Edge(p_a, t_2)
Inhibitor(p_n, t_1)


Or better look how SNAKES is doing this and hook into it
Being able to use SNAKES is a huge plus - my pnml generation can be improved


## Examples

Will output a lot of stuff
`./pygen.py examples/PetriModel.gm example/small_petri.grs`

Will put a pnml in a folder named "out" - maybe you need to create it first
`./grspnml.py examples/PetriModel.gm example/small_petri.grs`
