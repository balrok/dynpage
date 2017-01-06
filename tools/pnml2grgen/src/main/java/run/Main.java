package run;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class Main {
	public static void main(String[] args) {
		BaseConvert c;

		Path gfile;
		
		if (args[0].endsWith(".grsi")) {
			System.out.println("Converting from grgen to pnml");
			c = new grgen2pnml.Convert();
			gfile = Paths.get(args[0] + ".pnml");
			doConvert(c, gfile, args[0]);
			// System.out.println("Converting from grgen to net");
			// c = new grgen2net.Convert();
			// gfile = Paths.get(args[0] + ".net");
			// doConvert(c, gfile, args[0]);
		} else if (args[0].endsWith(".pnml")) {
			System.out.println("Converting from pnml to grgen");
			c = new pnml2grgen.Convert();
			gfile = Paths.get(args[0] + ".grsi");
			doConvert(c, gfile, args[0]);
		} else if (args[0].endsWith(".net")) {
			System.out.println("Converting from net to grgen");
			c = new net2grgen.Convert();
			gfile = Paths.get(args[0] + ".grsi");
			doConvert(c, gfile, args[0]);
		} else {
			System.err.println("You first argument should either end with '.grsi' or '.pnml'");
			return;
		}
	}
	
	protected static void doConvert(BaseConvert c, Path gfile, String in) {
		String converted_string = c.convertFile(in);
		if (converted_string == null) {
			System.err.println("Error with converting");
			return;
		}
		
		System.out.println(converted_string);
		
		try {
			Files.write(gfile, converted_string.getBytes("utf-8"), StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
