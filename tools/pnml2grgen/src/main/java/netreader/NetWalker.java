package netreader;

import parser.NetBaseListener;
import parser.NetParser;
import jnet.*;

public class NetWalker extends NetBaseListener {
	NetFile netFile;
	Node current;
	
	public NetWalker() {
		netFile = new NetFile();
	}

	@Override
	public void enterNetdesc(NetParser.NetdescContext ctx) {
		netFile.addDesc(new NetDesc(ctx.net().NAME() != null? ctx.net().NAME().getText() : ""));
	}
	
	protected Arc getArc(NetParser.ArcContext arc) {
		Arc ret = null;
		ret = new NormalArc("1");
		if (arc == null)
			return ret;
		if (arc.normal_arc() != null) {
			ret = new NormalArc();
			ret.setWeight(arc.normal_arc().weight().getText());
		}
		else if (arc.inhibitor_arc() != null) {
			ret = new InhibitorArc();
			ret.setWeight(arc.inhibitor_arc().weight().getText());
		}
		else if (arc.stopwatch_arc() != null) {
			ret = new StopwatchArc();
			ret.setWeight(arc.stopwatch_arc().weight().getText());
		}
		else if (arc.stopwatch_inhibitor_arc() != null) {
			ret = new StopwatchInhibitorArc();
			ret.setWeight(arc.stopwatch_inhibitor_arc().weight().getText());
		}
		else if (arc.test_arc() != null) {
			ret = new TestArc();
			ret.setWeight(arc.test_arc().weight().getText());
		}
		return ret;
	}

	@Override
	public void enterTrdesc(NetParser.TrdescContext ctx) {
		Transition tr = new Transition();
		if (ctx.transition().NAME() != null)
			tr.setName(ctx.transition().NAME().getText());
		if (ctx.label() != null)
			tr.setName(ctx.label().getText());
		if (ctx.interval() != null)
			tr.setInterval(ctx.interval().getText());

		for (NetParser.TinputContext ti : ctx.tinput()) {
			tr.addInPlace(new InPlace(ti.place().NAME().getText(), getArc(ti.arc())));
		}
		for (NetParser.ToutputContext to : ctx.toutput()) {
			tr.addInPlace(new InPlace(to.place().NAME().getText(),
					new NormalArc(to.normal_arc()!= null ? to.normal_arc().weight().getText() : "1")));
		}
		
		netFile.addDesc(tr);
		current = tr;
	}
}
