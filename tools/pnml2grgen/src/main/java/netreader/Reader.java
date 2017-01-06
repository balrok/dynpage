package netreader;

import java.io.IOException;

import org.antlr.v4.runtime.ANTLRFileStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import parser.NetLexer;
import parser.NetParser;
import jnet.NetFile;

public class Reader {
	public NetFile read(String fileName) {
		NetLexer lexer;
		System.err.println(fileName);
		try {
			lexer = new NetLexer(new ANTLRFileStream(fileName));
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		NetParser parser = new NetParser(tokens);
		ParseTree tree = parser.root();
		ParseTreeWalker walker = new ParseTreeWalker();
		NetWalker t = new NetWalker();
		walker.walk(t, tree);

		return t.netFile;
	}

}
