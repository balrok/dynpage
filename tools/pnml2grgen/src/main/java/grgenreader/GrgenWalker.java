package grgenreader;

import parser.GrsiBaseListener;
import parser.GrsiParser;
import parser.GrsiParser.ElementdeclContext;
import parser.GrsiParser.ParameterContext;
import parser.GrsiParser.ReferenceContext;
import jgrsi.Arc;
import jgrsi.Element;
import jgrsi.GrFile;
import jgrsi.Graph;
import jgrsi.Node;
import jgrsi.Parameter;

public class GrgenWalker extends GrsiBaseListener {

	public GrFile grsiFile;
	Element current_element;

	public GrgenWalker() {
		grsiFile = new GrFile();
	}

	@Override
	public void enterGraph(GrsiParser.GraphContext ctx) {
		String a = "";
		String b = "";
		if (ctx.name().size() > 1)
			b = ctx.name(1).getText();
		if (ctx.name().size() > 0)
			a = ctx.name(0).getText();
		grsiFile.addExpr(new Graph(a, b));
	}

	@Override
	public void enterNode(GrsiParser.NodeContext ctx) {
		String type = "";
		String id = "";
		type = ctx.elementdecl().name().getText();
		if (ctx.elementdecl().id() != null)
			id = ctx.elementdecl().id().getText();

		current_element = new Node(type, id, new jgrsi.List<Parameter>());
		grsiFile.addExpr(current_element);
	}

	@Override
	public void enterParameter(ParameterContext p) {
		current_element.addSimpleParameter(p.key().getText(), p.value().getText());
	}

	@Override
	public void enterArc(GrsiParser.ArcContext ctx) {
		String type = "";
		String id = "";
		ReferenceContext source = null;
		ReferenceContext target = null;
		ElementdeclContext e = null;

		boolean is_directed = true;
		if (ctx.directedarcleft() != null) {
			e = ctx.directedarcleft().elementdecl();
			source = ctx.reference(1);
			target = ctx.reference(0);
		} else {
			source = ctx.reference(0);
			target = ctx.reference(1);
			if (ctx.directedarcright() != null) {
				e = ctx.directedarcright().elementdecl();
			}
			if (ctx.undirectedarc() != null) {
				e = ctx.undirectedarc().elementdecl();
				is_directed = false;
			}
		}
		type = e.name().getText();
		if (e.id() != null)
			id = e.id().getText();

		current_element = 
				new Arc(type, id, new jgrsi.List<Parameter>(),
						source.getText(), target.getText(), is_directed);
		grsiFile.addExpr(current_element);
	}
}
