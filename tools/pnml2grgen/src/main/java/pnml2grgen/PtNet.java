package pnml2grgen;

import java.util.HashMap;
import java.util.Map;

import fr.lip6.move.pnml.ptnet.hlapi.ArcHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.PageHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.PetriNetHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.PlaceHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.PlaceNodeHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.PnObjectHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.RefPlaceHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.RefTransitionHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.TransitionHLAPI;
import fr.lip6.move.pnml.ptnet.hlapi.TransitionNodeHLAPI;
import jgrsi.Arc;
import jgrsi.GrFile;
import jgrsi.Graph;
import jgrsi.Node;
import jgrsi.Parameter;

public class PtNet extends PnmlReader {
	Map<Object, Node> mapped;
	GrFile grsiFile;
	Node petrinetNode;

	/**
	 * resources https://srcdev.lip6.fr/trac/research/ISOIEC-15909/wiki/English/User/HLAPI
	 * resources https://srcdev.lip6.fr/trac/research/ISOIEC-15909/wiki/English/User/Structure
	 * @param doc
	 * @throws Exception 
	 */
	public GrFile process(fr.lip6.move.pnml.ptnet.hlapi.PetriNetDocHLAPI doc) throws Exception {
		grsiFile = new GrFile();
		mapped = new HashMap<Object, Node>();
		grsiFile.addExpr(new Graph("Rules", "PnmlTest"));

		indl("doc:");
		indl(doc.toString());
		indl("nets:");
		indent();
		for (PetriNetHLAPI net : doc.getNetsHLAPI()) {
			processPetriNet(net);
		}
		unindent();
		return grsiFile;
	}

	protected void processPetriNet(PetriNetHLAPI net) throws Exception {
		petrinetNode = new Node("PetriNet", null, new jgrsi.List<Parameter>());
		petrinetNode.addSimpleParameter("$", getId(net));
		if (getLabel(net) != null)
			petrinetNode.addSimpleParameter("id", getLabel(net));
		grsiFile.addExpr(petrinetNode);
		
		printl(net);
		indl("pages:");
		indent();

		for (PageHLAPI page : net.getPagesHLAPI()) {
			processPage(page);
		}
		unindent();
	}

	protected void processPage(PageHLAPI page) throws Exception {
		Node ast = new Node("Page", null, new jgrsi.List<Parameter>());
		ast.addSimpleParameter("$", getId(page));
		if (getLabel(page) != null)
			ast.addSimpleParameter("id", getLabel(page));
		grsiFile.addExpr(ast);
		addMap(page, ast);

		Arc a = new Arc();
		a.setType("pages");
		if (page.getContainerPageHLAPI() != null) {
			a.setFromNode(getMap(page.getContainerPageHLAPI()));
		} else {
			a.setFromNode(petrinetNode);
		}
		a.setToNode(ast);
		a.setIsDirected(true);
		a.addSimpleParameter("$", genId());
		grsiFile.addExpr(a);

		printl(page);
		indent();
		for (PlaceHLAPI place : page.getObjects_PlaceHLAPI()) {
			processPlace(place);
		}
		for (RefPlaceHLAPI place : page.getObjects_RefPlaceHLAPI()) {
			processRefPlace(place);
		}
		
		for (TransitionHLAPI transition : page.getObjects_TransitionHLAPI()) {
			processTransition(transition);
		}
		for (RefTransitionHLAPI place : page.getObjects_RefTransitionHLAPI()) {
			processRefTransition(place);
		}

		for (PageHLAPI subpage : page.getObjects_PageHLAPI()) {
			processPage(subpage);
		}
		
		for (ArcHLAPI arc : page.getObjects_ArcHLAPI()) {
			processArc(arc);
		}
		unindent();
	}

	protected void processPlace(PlaceHLAPI place) throws Exception {
		Node ast = createAstNode(place, "Place", "places");

		if (place.getInitialMarkingHLAPI() != null) {
			long marking = place.getInitialMarkingHLAPI().getText();
			for (long i = 0; i < marking; i++) {
				Node tok = new Node("Token", null, new jgrsi.List<Parameter>());
				tok.addSimpleParameter("$", genId());
				grsiFile.addExpr(tok);
				Arc at = new Arc("tokens", null, new jgrsi.List<Parameter>(),
						ast.getId(), tok.getId(), true);
				at.addSimpleParameter("$", genId());
				grsiFile.addExpr(at);
				
			}
		}

		addMap(place, ast);
		printl(place);
	}

	protected void processRefPlace(RefPlaceHLAPI place) throws Exception {
		Node ast = createAstNode(place, "RefPlace", "places");

		PlaceNodeHLAPI referenced_place = place.getRefHLAPI();
		Arc aast = new Arc();
		aast.setType("edge_refplace");
		aast.setFromNode(ast);
		aast.setToNode(getMap(referenced_place));
		aast.setIsDirected(true);
		aast.addSimpleParameter("$", genId());
		grsiFile.addExpr(aast);
		
		addMap(place, ast);
		printl(place);
	}
	
	protected void processRefTransition(RefTransitionHLAPI transition) throws Exception {
		Node ast = createAstNode(transition, "RefTransition", "transitions");

		TransitionNodeHLAPI referenced_transition = transition.getRefHLAPI();
		Arc aast = new Arc();
		aast.setType("edge_reftransition");
		aast.setFromNode(ast);
		aast.setToNode(getMap(referenced_transition));
		aast.setIsDirected(true);
		aast.addSimpleParameter("$", genId());
		grsiFile.addExpr(aast);
		
		addMap(transition, ast);
		printl(transition);
	}

	protected void processTransition(TransitionHLAPI transition) throws Exception {
		Node ast = createAstNode(transition, "Transition", "transitions");
		addMap(transition, ast);
		printl(transition);
	}

	protected void processArc(ArcHLAPI arc) throws Exception {
		String type;
		if (arc.getSourceHLAPI() instanceof TransitionNodeHLAPI || arc.getTargetHLAPI() instanceof PlaceNodeHLAPI) {
			type = "inArc";
		} else if (arc.getSourceHLAPI() instanceof PlaceNodeHLAPI || arc.getTargetHLAPI() instanceof TransitionNodeHLAPI) {
			type = "outArc";
		} else {
			throw new Exception("Could not detect arc type");
		}

		Arc ast = new Arc();
		ast.setType(type);
		ast.setFromNode(getMap(arc.getSourceHLAPI()));
		ast.setToNode(getMap(arc.getTargetHLAPI()));
		ast.setIsDirected(true);
		ast.addSimpleParameter("$", getId(arc));
		if (getLabel(arc) != null)
			ast.addSimpleParameter("id", getLabel(arc));
		grsiFile.addExpr(ast);

		printl(arc);
	}

	// stupid workaround because HLAPI is not hashmappable
	// bugreport here: https://github.com/lhillah/pnmlframework/issues/9
	public void addMap(PnObjectHLAPI o, Node a) {
		mapped.put(o.getContainedItem(), a);
	}

	public Node getMap(PnObjectHLAPI o) throws Exception {
		Node n = mapped.get(o.getContainedItem());
		if (n == null) {
			throw new Exception("Not in map :" + o.getId());
		}
		return n;
	}

	protected String getLabel(PnObjectHLAPI o) {
		return getLabel(o, true);
	}
	protected String getLabel(PnObjectHLAPI o, Boolean quote) {
		String ret;
		if (o.getName() != null && !o.getName().getText().isEmpty()) {
			ret = o.getName().getText();
		} else {
			return null;
		}
		if (quote) {
			return '"'+ret+'"';
		}
		return ret;
	}
	protected String getLabel(PetriNetHLAPI o) {
		return getLabel(o, true);
	}
	protected String getLabel(PetriNetHLAPI o, Boolean quote) {
		String ret;
		if (o.getName() != null && !o.getName().getText().isEmpty()) {
			ret = o.getName().getText();
		} else {
			return null;
		}
		if (quote) {
			return '"'+ret+'"';
		}
		return ret;
	}

	protected void print(PnObjectHLAPI o) {
		if (!log)
			return;
		ind(getLabel(o));
	}

	protected void printl(PnObjectHLAPI o) {
		if (!log)
			return;
		print(o);
		System.out.println();
	}

	protected void printl(PetriNetHLAPI o) {
		if (!log)
			return;
		print(o);
		System.out.println();
	}

	protected void print(PetriNetHLAPI o) {
		if (!log)
			return;
		ind(getLabel(o));
	}

	protected void printl(ArcHLAPI o) {
		if (!log)
			return;
		print(o);
		System.out.println();
	}

	protected void print(ArcHLAPI o) {
		if (!log)
			return;
		ind(getLabel(o));
		noindent();
		System.out.print(" (");
		print(o.getSourceHLAPI());
		if (o.getInscriptionHLAPI() != null)
			System.out.print(" -" + o.getInscriptionHLAPI().getText() + "-> ");
		else
			System.out.print(" --> ");
		print(o.getTargetHLAPI());
		System.out.print(" )");
		restoreindent();
	}

	public String getId(PnObjectHLAPI o) {
		if (o.getId() != null)
			return "\""+o.getId()+'"';
		return genId();
	}

	public String getId(PetriNetHLAPI o) {
		if (o.getId() != null)
			return "\""+o.getId()+'"';
		return genId();
	}

	public Node createAstNode(PnObjectHLAPI o, String type, String arctype) throws Exception {
		Node ast = new Node(type, null, new jgrsi.List<Parameter>());
		ast.addSimpleParameter("$", getId(o));
		if (getLabel(o) != null)
			ast.addSimpleParameter("id", getLabel(o));
		grsiFile.addExpr(ast);
	
		Arc a = new Arc(arctype, null, new jgrsi.List<Parameter>(),
				getMap(o.getContainerPageHLAPI()).getId(), ast.getId(), true);
		a.addSimpleParameter("$", genId());
		grsiFile.addExpr(a);
		return ast;
	}
}
