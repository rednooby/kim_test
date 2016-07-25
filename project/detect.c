#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[])
{
	char cmd[100] = "python detect.py ";

	if (argc==1)
	{
		system(cmd);
	}
	else if (argc!=2)
	{
		fprintf(stderr, "Usage: %s [PATH TO DETECT]", argv[0]);
		return 1;
	}
	else
	{
		strncat(cmd, argv[1], 80);
		system(cmd);
	}
	return 0;
		//system("python detect.py %s", argv[1]);
	//printf("1234");
	//system("python detect.py");
}