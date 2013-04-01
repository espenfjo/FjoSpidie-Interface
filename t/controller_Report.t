use strict;
use warnings;
use Test::More;


use Catalyst::Test 'FjoSpidie';
use FjoSpidie::Controller::Report;

ok( request('/report')->is_success, 'Request should succeed' );
done_testing();
