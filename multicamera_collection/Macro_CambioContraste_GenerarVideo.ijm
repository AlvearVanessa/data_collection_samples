//VARIABLES
outputFolder="_Output"; //name of the output folder
batchMode=true; //to enable the background process //it is true, the macro does not work.

//PROCESS
print("\\Clear");
setBatchMode(batchMode);

//choose the folder
#@ File (label="Choose folder with the experiments", style="directory") directory

dirParent = File.getParent(directory);
dirName = File.getName(directory);
dirOutput = dirParent+File.separator+dirName+outputFolder;
if (File.exists(dirOutput)==false) {
  File.makeDirectory(dirOutput); // new output folder
}

print("Starting...");
listDirectories = getFileList(directory);
print("number of directories in the folder: "+listDirectories.length);

for(a=0;a<listDirectories.length;a++)//a es cada carpeta E?
{
	indexSlash= lastIndexOf(listDirectories[a], "/"); 
	aux=substring(listDirectories[a],0, indexSlash);
	pathExp=aux;
	dirExp=directory+File.separator+listDirectories[a];
	listFiles=getFileList(dirExp);
	
	dirOutputFrames = directory+File.separator+pathExp+outputFolder;
	if (File.exists(dirOutputFrames)==false) {
	  File.makeDirectory(dirOutputFrames); // new output folder
	}

	for (i=0; i<listFiles.length; i++) //list.length
	{
	     pathI=dirExp+File.separator+listFiles[i];

	     //only tif-files
	     indexExt= lastIndexOf(listFiles[i], "."); //indexOf(string, substring) Returns the index within string of the last occurrence of substring
	     extension= substring(listFiles[i], indexExt);
	     if(extension==".png"){
			open(dirExp+File.separator+File.separator+listFiles[i]);
			title=getTitle();
			run("Enhance Contrast...", "saturated=0.35 equalize");
			saveAs("PNG", dirOutputFrames+File.separator+title);
			close();
	     
		}
	}
	
	File.openSequence(dirOutputFrames);
	run("AVI... ", "compression=JPEG frame=30 save="+dirOutput+File.separator+pathExp+".avi");
	print(dirOutput+File.separator+pathExp+".avi");
	
}

print("done!");