class Test
{
    public static void test(String[] args)
    {
        System.out.println("Hello World");
    }
}

class Feb14
{
    public static void main(String[] ars)
    {
        int x = 2;
        int y, z;
        y = 764321;
        z = x + y;
        System.out.println(x+ "+" +y+ "=" +z);
        System.out.println(5 + "+" + 7 + "=" + 5+7);
        System.out.println(5 + "+" + 7 + "=" + (5+7));

        double score = 89.5;
        char letterGrade = calcGrade(score);
        System.out.println("A score of " + score + " is a/an " + letterGrade);
        commentGrade(letterGrade);
    }
    private static char calcGrade(double value)
    {
        if (value >= 90)
            return 'A';
        else if (value >= 80)
            return 'B';
        else if (value >= 70)
            return 'C';
        else if (value >= 60)
            return 'D';
        else
            return 'F';

    }
    //function that recives a letter grafe and prints out an approriate comment
    //eg. Good Job, better luck next time, see me asap
    private static void commentGrade(char grade)
    {
        if (grade == 'A' || grade == 'B')
            System.out.println("Good Job");
        else if (grade == 'C' || grade == 'D')
            System.out.println("Better Luck Next Time");
        else
            System.out.println("See Me ASAP");
    }
}