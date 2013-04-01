use utf8;
package FjoSpidie::Schema::Result::Response;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

FjoSpidie::Schema::Result::Response

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

=back

=cut

__PACKAGE__->load_components("InflateColumn::DateTime");

=head1 TABLE: C<response>

=cut

__PACKAGE__->table("response");

=head1 ACCESSORS

=head2 id

  data_type: 'mediumint'
  is_auto_increment: 1
  is_nullable: 0

=head2 entry_id

  data_type: 'mediumint'
  is_foreign_key: 1
  is_nullable: 0

=head2 httpversion

  data_type: 'blob'
  is_nullable: 1

=head2 statustext

  data_type: 'blob'
  is_nullable: 1

=head2 status

  data_type: 'integer'
  is_nullable: 1

=head2 bodysize

  data_type: 'integer'
  is_nullable: 1

=head2 headersize

  data_type: 'integer'
  is_nullable: 1

=cut

__PACKAGE__->add_columns(
  "id",
  { data_type => "mediumint", is_auto_increment => 1, is_nullable => 0 },
  "entry_id",
  { data_type => "mediumint", is_foreign_key => 1, is_nullable => 0 },
  "httpversion",
  { data_type => "blob", is_nullable => 1 },
  "statustext",
  { data_type => "blob", is_nullable => 1 },
  "status",
  { data_type => "integer", is_nullable => 1 },
  "bodysize",
  { data_type => "integer", is_nullable => 1 },
  "headersize",
  { data_type => "integer", is_nullable => 1 },
);

=head1 PRIMARY KEY

=over 4

=item * L</id>

=back

=cut

__PACKAGE__->set_primary_key("id");

=head1 RELATIONS

=head2 entry

Type: belongs_to

Related object: L<FjoSpidie::Schema::Result::Entry>

=cut

__PACKAGE__->belongs_to(
  "entry",
  "FjoSpidie::Schema::Result::Entry",
  { id => "entry_id" },
  { is_deferrable => 1, on_delete => "RESTRICT", on_update => "RESTRICT" },
);


# Created by DBIx::Class::Schema::Loader v0.07035 @ 2013-03-29 12:01:28
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:EwPycGsbZxQhgJ62zmoc4Q


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;
