package net2grgen;

import java.util.HashMap;
import java.util.Map;

import jnet.*;
import jgrsi.Arc;
import jgrsi.GrFile;
import jgrsi.Graph;
import jgrsi.Node;
import jgrsi.Parameter;

public class Mapper {
	Map<jnet.Node, jgrsi.Node> mapped;
	Node pageNode;
	GrFile grsiFile;
	public int id_counter;

	public Mapper() {
		mapped = new HashMap<jnet.Node, jgrsi.Node>();
		id_counter = 0;
	}

	public GrFile convert(NetFile netFile) throws Exception {
		grsiFile = new GrFile();
		grsiFile.addExpr(new Graph("Rules", "NetTest"));
		
		for (Desc desc : netFile.getDescs()) {
			if (desc instanceof NetDesc) {
				Node petrinetNode = new jgrsi.Node("PetriNet", null, new jgrsi.List<Parameter>());
				petrinetNode.addSimpleParameter("$", genId());
				petrinetNode.addSimpleParameter("id", ((NetDesc) desc).getName());
				grsiFile.addExpr(petrinetNode);
				pageNode = new Node();
				pageNode.setType("Page");
				pageNode.addSimpleParameter("$", genId());

				Arc a = new Arc("pages", null, new jgrsi.List<Parameter>(),
						petrinetNode.getId(), pageNode.getId(), true);
				a.addSimpleParameter("$", genId());
				grsiFile.addExpr(a);
				grsiFile.addExpr(pageNode);
			}
			if (desc instanceof Transition) {
				createAstNode((Transition)desc, "Transition", "transitions");
			}
			if (desc instanceof Place) {
				createAstNode((Place)desc, "Place", "places");
			}
		}
		return grsiFile;
	}
	
	public String getId(jnet.Node n) {
		if (!n.getName().isEmpty()) {
			return n.getName();
		}
		return genId();
	}
	public String genId() {
		id_counter++;
		return String.format("\"$%X\"", id_counter);
	}
	

	public Node createAstNode(jnet.Node n, String type, String arctype) throws Exception {
		Node ast = new Node(type, null, new jgrsi.List<Parameter>());
		ast.addSimpleParameter("$", getId(n));
		if (!n.getName().isEmpty())
			ast.addSimpleParameter("id", n.getName());
		grsiFile.addExpr(ast);
	
		Arc a = new Arc(arctype, null, new jgrsi.List<Parameter>(),
				pageNode.getId(), ast.getId(), true);
		a.addSimpleParameter("$", genId());
		grsiFile.addExpr(a);
		return ast;
	}
}
