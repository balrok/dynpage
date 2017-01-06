package all;

import org.apache.commons.lang3.StringUtils;
import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import run.BaseConvert;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class AllTest {

    @DataProvider(name = "pnml2grgen")
    public static Iterator<Object[]> pnml2grgenProvider() {
        return folderProvider("src/test/resources/pnml2grgen");
    }
    
    @DataProvider(name = "grgen2pnml")
    public static Iterator<Object[]> grgen2pnmlProvider() {
        return folderProvider("src/test/resources/grgen2pnml");
    }

    public static Iterator<Object[]> folderProvider(String dir) {
        List<Object[]> files = new ArrayList<Object[]>();
    	Path p = Paths.get(dir);
    	System.out.println("check dir "+dir);
    	try {
			Files.list(p)
		            .filter(path -> Files.isRegularFile(path))
		            .filter(path -> !path.getFileName().toString().endsWith(".test"))
		            .sorted((path1, path2) -> path1.getFileName().compareTo(path2.getFileName()))
		            .forEach(path -> {
		            	Path g = Paths.get(path.toString()+".test");
		            	if (Files.exists(g)) {
		            		files.add(new Object[]{path, g});
		            	} else {
		            		files.add(new Object[]{path, null});
		            	}
		            });;
		} catch (IOException e) {
			e.printStackTrace();
			System.err.println("Directory " + dir + " does not exist");
		    System.err.println("Working Directory = " + System.getProperty("user.dir"));
			return null;
		}
        return files.iterator();
    }

    @Test(dataProvider = "pnml2grgen", groups = {"pnml2grgen"})
    public void testPnmlParser(Path p, Path g) throws Exception {
        // printFile(p);
        BaseConvert c = new pnml2grgen.Convert();
        test(c, p, g);
    }
    
    @Test(dataProvider = "grgen2pnml", groups = {"grgen2pnml"})
    public void testGrgenParser(Path p, Path g) throws Exception {
        //printFile(p);
        BaseConvert c = new grgen2pnml.Convert();
        test(c, p, g);
    }

    @Test(dataProvider = "grgen2pnml", groups = {"grgen2pnml", "pnml2grgen"})
    public void testGrgenParserBothDirections(Path p, Path g) throws Exception {
        BaseConvert c = new grgen2pnml.Convert();
        BaseConvert c2 = new pnml2grgen.Convert();
		testBoth(c, c2, p);
    }

    protected void printFile(Path p) throws Exception {
		System.out.println(String.join("\n", Files.readAllLines(p)));
    }

    private void test(BaseConvert c, Path p, Path gold) throws Exception {
		// uncomment this if you want to override
		// gold = null;
        Assert.assertTrue(Files.exists(p));
        
        String result = c.convertFile(p.toString());
        Assert.assertNotEquals(result, "");
        Assert.assertNotEquals(result, null);
        if (gold != null) {  
        	String diff = StringUtils.difference(result, String.join("\n", Files.readAllLines(gold)));
        	Assert.assertEquals(diff, "");
        } else {
        	Path gfile = Paths.get(p.toString() + ".test");
    		try {
    			Files.write(gfile, result.getBytes("utf-8"), StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
    		} catch(Exception e) {}
        }
    }

	/**
	 * Will convert multiple times and compares against itself
	 * first convert with c, then with c2 then again c
	 */
    private void testBoth(BaseConvert c, BaseConvert c2, Path p) throws Exception {
        Assert.assertTrue(Files.exists(p));
        
        String result = c.convertFile(p.toString());
        Assert.assertNotEquals(result, "");
        Assert.assertNotEquals(result, null);
        String result2 = c2.convertString(result);
        Assert.assertNotEquals(result2, "");
        Assert.assertNotEquals(result2, null);

		String diff = StringUtils.difference(String.join("\n", Files.readAllLines(p)).trim(), result2.trim());
		Assert.assertEquals(diff, "");
    }
}
