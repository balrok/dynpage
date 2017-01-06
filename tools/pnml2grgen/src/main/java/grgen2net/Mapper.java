package grgen2net;

import java.util.HashMap;
import java.util.Map;

import jgrsi.*;
import jnet.NetFile;

public class Mapper {
	Map<jgrsi.Node, jnet.Node> mapped;

	public Mapper() {
		mapped = new HashMap<jgrsi.Node, jnet.Node>();
	}

	public jnet.NetFile convert(GrFile grsiFile) throws Exception {
		NetFile nf = new NetFile();
		for (Expr expr : grsiFile.getExprs()) {
			if (expr instanceof Node && ((Node) expr).getType().equals("PetriNet")) {
				convertNet((Node) expr, nf);
			}
		}
		return nf;
	}
	
	public void convertNet(jgrsi.Node n, jnet.NetFile nf) {
		jnet.NetDesc nd = new jnet.NetDesc();
		if (n.getParameterByKey("id") != null) {
			n.setName(n.getParameterByKey("id").getValue());
		}
		nf.addDesc(nd);
		for (Arc arcpn : n.getOutArcs()) {
			if (arcpn.getToNode() != null && arcpn.getToNode().getType().equals("Page")) {
				Node page = arcpn.getToNode();
				for (Arc arc : page.getOutArcs()) {
					if (arc.getToNode() != null) {
						switch (arc.getToNode().getType()) {
							case "Place":
								convertPlace(arc.getToNode(), nf);
								break;
							case "Transition":
								convertTransition(arc.getToNode(), nf);
								break;
						}
					}
				}
			}
			
		}
	}
	
	public void convertPlace(Node n, jnet.NetFile nf) {
		Integer tokens = 0;
		for (Arc arc : n.getOutArcs()) {
			if (arc.getToNode() != null) {
				if (arc.getToNode().getType().equals("Token")) {
					tokens++;
				}
			}
		}
		if (tokens > 0) {
			jnet.Place pl = new jnet.Place();
			pl.setMarking(tokens);
			if (n.getId() != null) {
				pl.setName(n.getId());
			}
			nf.addDesc(pl);
		}
	}
	
	public void convertTransition(Node n, jnet.NetFile nf) {
		jnet.Transition tr = new jnet.Transition();
		if (n.getId() != null) {
			tr.setName(n.getId());
		}
		for (Arc arc : n.getInArcs()) {
			if (arc.getFromNode().getType().equals("Place")) {
				jnet.InPlace ip = new jnet.InPlace();
				ip.setName(arc.getFromNode().getId());
				if (arc.getType().equals("inhibitorArc")) {
					ip.setArcType(new jnet.InhibitorArc());
				}
				tr.addInPlace(ip);
			}
		}
		for (Arc arc : n.getOutArcs()) {
			if (arc.getToNode().getType().equals("Place")) {
				jnet.OutPlace op = new jnet.OutPlace();
				op.setName(arc.getFromNode().getId());
				tr.addOutPlace(op);
			}
		}
		nf.addDesc(tr);	
	}
}
