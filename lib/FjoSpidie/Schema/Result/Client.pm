use utf8;
package FjoSpidie::Schema::Result::Client;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

FjoSpidie::Schema::Result::Client

=cut

use strict;
use warnings;

use Moose;
use MooseX::NonMoose;
use MooseX::MarkAsMethods autoclean => 1;
extends 'DBIx::Class::Core';

=head1 COMPONENTS LOADED

=over 4

=item * L<DBIx::Class::InflateColumn::DateTime>

=item * L<DBIx::Class::TimeStamp>

=item * L<DBIx::Class::PassphraseColumn>

=back

=cut

__PACKAGE__->load_components("InflateColumn::DateTime", "TimeStamp", "PassphraseColumn");

=head1 TABLE: C<clients>

=cut

__PACKAGE__->table("clients");

=head1 ACCESSORS

=head2 username

  data_type: 'varchar'
  default_value: (empty string)
  is_nullable: 0
  size: 25

=head2 passwd

  data_type: 'blob'
  is_nullable: 1

=head2 groups

  data_type: 'varchar'
  default_value: (empty string)
  is_nullable: 0
  size: 25

=head2 user_id

  data_type: 'mediumint'
  is_auto_increment: 1
  is_nullable: 0

=cut

__PACKAGE__->add_columns(
  "username",
  { data_type => "varchar", default_value => "", is_nullable => 0, size => 25 },
  "passwd",
  { data_type => "blob", is_nullable => 1 },
  "groups",
  { data_type => "varchar", default_value => "", is_nullable => 0, size => 25 },
  "user_id",
  { data_type => "mediumint", is_auto_increment => 1, is_nullable => 0 },
);

=head1 PRIMARY KEY

=over 4

=item * L</user_id>

=back

=cut

__PACKAGE__->set_primary_key("user_id");


# Created by DBIx::Class::Schema::Loader v0.07035 @ 2013-03-29 20:03:07
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:kuOwGpqYevWlCazQC8CzDg

# Have the 'password' column use a SHA-1 hash and 20-byte salt
# with RFC 2307 encoding; Generate the 'check_password" method
__PACKAGE__->add_columns(
    'passwd' => {
        passphrase       => 'rfc2307',
        passphrase_class => 'SaltedDigest',
        passphrase_args  => {
            algorithm   => 'SHA-1',
        },
        passphrase_check_method => 'check_password',        
    },
);


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;
