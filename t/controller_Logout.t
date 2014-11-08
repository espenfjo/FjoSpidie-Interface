use strict;
use warnings;
use Test::More;

use Catalyst::Test 'FjoSpidie';
use FjoSpidie::Controller::Logout;

ok( request('/logout')->is_redirect, 'Request should succeed' );
done_testing();
