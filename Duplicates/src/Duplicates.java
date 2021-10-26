/* Samson Nguyen 330612 1001496565 */
/* Standard Results:               */
/* Method 1 Search Average:	60 ms  */
/* Method 2 Search Average:	14 ms  */
/* Method 3 Search Average:	66 ms  */

/* Find the number of duplicate numbers in  */
/* two randomly populated sorted arrays.    */
/* Do not count duplicates more than once.  */

import java.util.Arrays;

public class Duplicates {
    private static int size = 1000000;

    public static void main(String[] args) {
        int iterations = 100;

        long avg1 = 0;
        long avg2 = 0;
        long avg3 = 0;

        for (int x = 0; x < iterations; x++) {
            // instantiate new int arrays

            int[] nums1 = new int[size];
            int[] nums2 = new int[size];

            // fill arrays with random numbers
            for (int i = 0; i < size; i++) {
                nums1[i] = (int) (Math.random() * (10 * size) + 1);
                nums2[i] = (int) (Math.random() * (10 * size) + 1);
            }

            // sort arrays
            Arrays.sort(nums1);
            Arrays.sort(nums2);

            // x'th iteration of three methods running from x = 0
            System.out.println("Iteration " + (x + 1) + ":");

            // start time
            long time = System.currentTimeMillis();

            // call binary search method
            int duplicates = BinaryMethod(nums1, nums2);

            // end time
            time = System.currentTimeMillis() - time;
            System.out.println("Binary Search Method:");
            System.out.println("\tTime taken:\t" + time + " ms");
            System.out.println("\tDuplicates:\t" + duplicates);
            // add to average sum
            avg1 += time;

            time = System.currentTimeMillis();

            duplicates = MyMethod(nums1, nums2);

            time = System.currentTimeMillis() - time;
            System.out.println("My Search Method:");
            System.out.println("\tTime taken:\t" + time + " ms");
            System.out.println("\tDuplicates:\t" + duplicates);
            avg2 += time;

            time = System.currentTimeMillis();

            duplicates = InterpolationMethod(nums1, nums2);

            time = System.currentTimeMillis() - time;
            System.out.println("Interpolation Search Method:");
            System.out.println("\tTime taken:\t" + time + " ms");
            System.out.println("\tDuplicates:\t" + duplicates);
            avg3 += time;

            System.out.println();
        }

        avg1 /= iterations;
        avg2 /= iterations;
        avg3 /= iterations;

        System.out.println("Method 1 Search Average:\t" + avg1 + " ms");
        System.out.println("Method 2 Search Average:\t" + avg2 + " ms");
        System.out.println("Method 3 Search Average:\t" + avg3 + " ms");
    }

    // for each i, binary search a2 for a1[i]
    private static int BinaryMethod(int[] a1, int[] a2) {
        int result = 0;
        for (int i = 0; i < size; i++) {
            if (i > 0 && a1[i] == a1[i - 1]) {
                continue;
            }
            if (Arrays.binarySearch(a2, a1[i]) > -1) {
                result++;
            }
        }
        return result;
    }

    // increase j until a2[j] > a1[i],
    // then increase i until a1[i] > a2[j].
    // result++ whenever a1[i] == a2[j].
    private static int MyMethod(int[] a1, int[] a2) {
        int result = 0;
        int currentIndex = 0;
        boolean flagComplete = false;
        for (int i = 0; i < size; i++) {
            // if already checked, continue
            if (i > 0 && a1[i] == a1[i - 1]) {
                continue;
            }
            while (i < size-1 && a1[i] < a2[currentIndex]) {
                i++;
            }
            for (int j = currentIndex; j < size; j++) {
                // if already checked, continue
                if (j > 0 && a2[j] == a2[j - 1]) {
                    while (j < size-1 && a2[j] == a2[j - 1]) {
                        j++;
                    }
                }
                // if smaller than goal, continue
                else if (a2[j] < a1[i]) {
                    while (j < size-1 && a2[j] < a1[i]) {
                        j++;
                    }
                }
                // if bigger than goal, reassign minimum index and break
                if (a2[j] > a1[i]) {
                    currentIndex = j;
                    break;
                }
                // if duplicate, add to duplicate set
                if (a1[i] == a2[j]) {
                    result++;
                }
                // if reached maximum index, end loop
                if (j == size-1) {
                    flagComplete = true;
                }
            }
            if (flagComplete) {
                break;
            }
        }
        return result;
    }

    // elements sorted and uniformly distributed
    // start index = 0, end index = size-1
    // position (pos) = start + ((end-start)/(a2[end]-a2[start])) * (e - a2[start])
    //  where e is element being searched for
    // result++ if a2[pos] == e
    // if e > a2[pos], start = pos + 1
    // else end = pos - 1
    private static int InterpolationMethod(int[] a1, int[] a2) {
        int result = 0;
        int pos;
        for (int i = 0; i < size; i++) {
            if (i > 0 && a1[i] == a1[i - 1]) {
                continue;
            }
            int start = 0;
            int end = size-1;
            while (start <= end && a1[i] >= a2[start] && a1[i] <= a2[end]) {
                pos = start + (int) ((double) (end - start) / (double) (a2[end] - a2[start]) * (a1[i] - a2[start]));
                if (a2[pos] == a1[i]) {
                    result++;
                    break;
                } else if (a1[i] > a2[pos]) {
                    start = pos + 1;
                } else {
                    end = pos - 1;
                }
            }
        }
        return result;
    }
}
