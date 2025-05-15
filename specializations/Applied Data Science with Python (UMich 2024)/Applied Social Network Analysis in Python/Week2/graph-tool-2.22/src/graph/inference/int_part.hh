// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#ifndef INT_PART_HH
#define INT_PART_HH

#include "config.h"

#include <cmath>
#include <iostream>
#include <boost/multi_array.hpp>

#include "cache.hh"

namespace graph_tool
{
using namespace boost;

void init_q_cache(size_t n_max);
double q_rec(int n, int k);
double q_rec_memo(int n, int k);
double log_q_approx(int n, int k);
double log_q_approx_big(int n, int k);
double log_q_approx_small(int n, int k);

extern boost::multi_array<double, 2> __q_cache;

template <class T>
double log_q(T n, T k)
{
    if (n <= 0 || k < 1)
        return 0;
    if (k > n)
        k = n;
    if (n < T(__q_cache.shape()[0]))
        return __q_cache[n][k];
    return log_q_approx(n, k);
}

}
#endif // INT_PART_HH
