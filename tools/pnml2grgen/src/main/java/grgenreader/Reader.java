package grgenreader;

import java.io.IOException;

import org.antlr.v4.runtime.ANTLRFileStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import parser.GrsiLexer;
import parser.GrsiParser;
import jgrsi.GrFile;

public class Reader {
	public GrFile read(String fileName) {
		GrsiLexer lexer;
		System.err.println(fileName);
		try {
			lexer = new GrsiLexer(new ANTLRFileStream(fileName));
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		GrsiParser parser = new GrsiParser(tokens);
		ParseTree tree = parser.root();
		ParseTreeWalker walker = new ParseTreeWalker();
		GrgenWalker t = new GrgenWalker();
		walker.walk(t, tree);

		return t.grsiFile;
	}

}
