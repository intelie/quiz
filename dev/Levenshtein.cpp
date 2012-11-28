
#include "Levenshtein.h"



int Levenshtein::distance(const QString& first, const QString& second)
{
    /*
     * http://en.wikipedia.org/wiki/Levenshtein_distance
     */

    const int first_length = first.length();
    const int second_length = second.length();

    if (!first_length) return first_length;
    if (!second_length) return second_length;

    QVector<int> costs(second_length + 1);
    for (size_t k = 0; k <= second_length; k++) costs[k] = k;


    for (int i = 0; i < first_length; i++) {
        costs[0] = i + 1;
        int corner = i;
        for (int j = 0; j < second_length; j++) {
            int upper = costs[j + 1];

            if (first[i] == second[j]) {
                costs[j + 1] = corner;
            }

            else {
                const int temp = upper < corner ? upper : corner;
                costs[j + 1] = (costs[j] < temp ? costs[j] : temp) + 1;
            }

            corner = upper;
        }
    }

    return costs[second_length];
}
