package pnml2grgen;

import org.apache.commons.lang3.StringUtils;

public class PnmlReader {
	public int level;
	public int old_level;
	public boolean log = false;
	public int id_counter;

	public PnmlReader() {
		level = 0;
		old_level = 0;
		id_counter = 0;
	}

	protected void indl(String s) {
		if (!log)
			return;
		System.out.println(StringUtils.repeat("  ", level) + s);
	}

	protected void ind(String s) {
		if (!log)
			return;
		System.out.print(StringUtils.repeat("  ", level) + s);
	}

	public void indent() {
		level++;
	}

	public void unindent() {
		level--;
	}

	public void noindent() {
		old_level = level;
		level = 0;
	}

	public void restoreindent() {
		level = old_level;
	}

	public String genId() {
		id_counter++;
		return String.format("\"$%X\"", id_counter);
	}
	
}
