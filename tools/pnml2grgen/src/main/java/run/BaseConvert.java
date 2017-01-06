package run;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public abstract class BaseConvert {
	public abstract String convertFile(String fileName);
	
	
	public String convertString(String str) {
		String fileName = "";
		try {
			Path tmp =  Files.createTempFile("tmp", ".tmp");
			fileName = tmp.toAbsolutePath().toString();
            Files.write(tmp, str.getBytes("utf-8"), StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
		return convertFile(fileName);
	}
}
