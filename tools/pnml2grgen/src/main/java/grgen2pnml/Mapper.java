package grgen2pnml;

import java.util.HashMap;
import java.util.Map;

import fr.lip6.move.pnml.framework.utils.ModelRepository;
import fr.lip6.move.pnml.framework.utils.exception.InvalidIDException;
import fr.lip6.move.pnml.framework.utils.exception.VoidRepositoryException;
import fr.lip6.move.pnml.ptnet.hlapi.*;

import jgrsi.*;

public class Mapper {
	Map<Node, NodeHLAPI> mapped;

	public Mapper() {
		mapped = new HashMap<Node, NodeHLAPI>();
	}

	public PetriNetDocHLAPI convert(GrFile grsiFile) throws Exception {

		ModelRepository.getInstance().reset();
		ModelRepository.getInstance().createDocumentWorkspace("void");
		PetriNetDocHLAPI doc = new PetriNetDocHLAPI();
		for (Expr expr : grsiFile.getExprs()) {
			if (expr instanceof Node && ((Node) expr).getType().equals("PetriNet")) {
				convertNet((Node) expr, doc);
			}
		}
		for (Expr expr : grsiFile.getExprs()) {
			if (expr instanceof Arc) {
				Arc a = (Arc) expr;
				switch (a.getType()) {
				case "inArc":
				case "outArc":
					convertArc(a);
					break;
				}
			}
		}
		return doc;
	}

	public void convertNet(Node n, PetriNetDocHLAPI doc) throws Exception {
		PetriNetHLAPI net = new PetriNetHLAPI(getXmlId(n), PNTypeHLAPI.PTNET, null, doc);
		net.setNameHLAPI(getNameHLAPI(n.getLabel()));
		for (Arc arc : n.getOutArcs()) {
			if (arc.getToNode() != null && arc.getToNode().getType().equals("Page")) {
				convertPage(arc.getToNode(), net);
			}
		}
	}

	public void convertPage(Node n, PetriNetHLAPI net) throws Exception {
		PageHLAPI page = new PageHLAPI(getXmlId(n), null, null, net); //use of "null" is authorized but not encouraged 
		page.setNameHLAPI(getNameHLAPI(n.getLabel()));
		convertPageChildren(n, page);
	}

	public void convertPage(Node n, PageHLAPI pag) throws Exception {
		PageHLAPI page = new PageHLAPI(getXmlId(n), null, null, pag); //use of "null" is authorized but not encouraged 
		page.setNameHLAPI(getNameHLAPI(n.getLabel()));
		convertPageChildren(n, page);
	}

	public void convertPageChildren(Node n, PageHLAPI page) throws Exception {
		for (Arc arc : n.getOutArcs()) {
			if (arc.getToNode() != null) {
				switch (arc.getToNode().getType()) {
					case "Place":
						convertPlace(arc.getToNode(), page);
						break;
					case "RefPlace":
						convertRefPlace(arc.getToNode(), page);
						break;
					case "RefTransition":
						convertRefTransition(arc.getToNode(), page);
						break;
					case "Transition":
					case "PriorityTransition": // TODO would need some special handling
						convertTransition(arc.getToNode(), page);
						break;
					case "Page":
						convertPage(arc.getToNode(), page);
						break;
				}
			}
		}
	}

	public void convertPlace(Node n, PageHLAPI page) throws InvalidIDException, VoidRepositoryException {
		PlaceHLAPI place = new PlaceHLAPI(getXmlId(n));
		convertNode(n, place, page);
		long tokens = 0;
		for (Arc arc : n.getOutArcs()) {
			if (arc.getToNode() != null) {
				if (arc.getToNode().getType().equals("Token")) {
					tokens++;
				}
			}
		}
		if (tokens > 0) {
			place.setInitialMarkingHLAPI(new PTMarkingHLAPI(tokens));
		}
	}

	public void convertRefPlace(Node n, PageHLAPI page) throws Exception {
		PlaceNodeHLAPI referenced_place = null;

		for (Arc arc : n.getOutArcs()) {
			if (arc.getType().equals("edge_refplace") && arc.getToNode() != null) {
				referenced_place = (PlaceNodeHLAPI) mapped.get(arc.getToNode());
				break;
			}
		}
		if (referenced_place == null) {
			throw new Exception("Referenced Place is null");
		}
		RefPlaceHLAPI place = new RefPlaceHLAPI(getXmlId(n), referenced_place);
		convertNode(n, place, page);
	}
	
	public void convertRefTransition(Node n, PageHLAPI page) throws Exception {
		TransitionNodeHLAPI referenced_transition = null;

		for (Arc arc : n.getOutArcs()) {
			if (arc.getType().equals("edge_reftransition") && arc.getToNode() != null) {
				referenced_transition = (TransitionNodeHLAPI) mapped.get(arc.getToNode());
				break;
			}
		}
		if (referenced_transition == null) {
			throw new Exception("Referenced Transition is null");
		}
		RefTransitionHLAPI transition = new RefTransitionHLAPI(getXmlId(n), referenced_transition);
		convertNode(n, transition, page);
	}

	public void convertTransition(Node n, PageHLAPI page) throws InvalidIDException, VoidRepositoryException {
		TransitionHLAPI transition = new TransitionHLAPI(getXmlId(n));
		convertNode(n, transition, page);
	}

	public void convertNode(Node n, NodeHLAPI node, PageHLAPI page) {
		node.setNameHLAPI(getNameHLAPI(n.getLabel()));
		node.setContainerPageHLAPI(page);
		mapped.put(n, node);
	}

	public void convertArc(Arc a) throws InvalidIDException, VoidRepositoryException {
		if (a.getFromNode() == null) {
			System.err.println("Arc "+a.getPlainId()+" has no fromnode");
		}
		if (a.getToNode() == null) {
			System.err.println("Arc "+a.getPlainId()+" has no tonode");
		}
		if (mapped.get(a.getFromNode()) == null) {
			System.err.println("Fromnode "+a.getFromNode().getPlainId()+" of Arc "+a.getPlainId()+" is not in mapping");
		}
		if (mapped.get(a.getToNode()) == null) {
			System.err.println("Tonode "+a.getToNode().getPlainId()+" of Arc "+a.getPlainId()+" is not in mapping");
		}
		new ArcHLAPI(getXmlId(a), mapped.get(a.getFromNode()), mapped.get(a.getToNode()),
				mapped.get(a.getFromNode()).getContainerPageHLAPI());
	}

	public String getXmlId(Element e) {
		return e.getPlainId().replaceAll("[^a-zA-Z0-9\\-_.]", "_").replaceAll("^[^a-zA-Z]", "id$0");
	}
	
	public NameHLAPI getNameHLAPI(String s) {
		if (s == null)
			return null;
		// it is no valid pnml-core when there is no graphic attached to the name-label
		// return new NameHLAPI(new AnnotationGraphicsHLAPI(new OffsetHLAPI(0, 0), null, null, null), s);
		return new NameHLAPI(s);
	}
}
