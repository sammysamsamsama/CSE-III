/* Samson Nguyen 1001496565 */

/* This program converts decimal to binary */

/* divide by 2 ignore the remainder. even = 0, odd = 1 */

#include <stdio.h>

int main(void)
{
    int num;
    printf("Enter a decimal integer : ");
    scanf("%d", &num);
    char[] binaryNum = "";
    while (num > 0)
    {
        if (num % 2 == 0)
        {
            binaryNum = "0" + binaryNum;
        }
        else
        {
            binaryNum = "1" + binaryNum;
        }
    }
    printf(binaryNum);
    return 0;
}