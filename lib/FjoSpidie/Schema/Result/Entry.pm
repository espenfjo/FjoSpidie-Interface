use utf8;
package FjoSpidie::Schema::Result::Entry;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

FjoSpidie::Schema::Result::Entry

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

=head1 TABLE: C<entry>

=cut

__PACKAGE__->table("entry");

=head1 ACCESSORS

=head2 id

  data_type: 'mediumint'
  is_auto_increment: 1
  is_nullable: 0

=head2 report_id

  data_type: 'mediumint'
  is_foreign_key: 1
  is_nullable: 0

=cut

__PACKAGE__->add_columns(
  "id",
  { data_type => "mediumint", is_auto_increment => 1, is_nullable => 0 },
  "report_id",
  { data_type => "mediumint", is_foreign_key => 1, is_nullable => 0 },
);

=head1 PRIMARY KEY

=over 4

=item * L</id>

=back

=cut

__PACKAGE__->set_primary_key("id");

=head1 RELATIONS

=head2 headers

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Header>

=cut

__PACKAGE__->has_many(
  "headers",
  "FjoSpidie::Schema::Result::Header",
  { "foreign.entry_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 report

Type: belongs_to

Related object: L<FjoSpidie::Schema::Result::Report>

=cut

__PACKAGE__->belongs_to(
  "report",
  "FjoSpidie::Schema::Result::Report",
  { id => "report_id" },
  { is_deferrable => 1, on_delete => "RESTRICT", on_update => "RESTRICT" },
);

=head2 requests

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Request>

=cut

__PACKAGE__->has_many(
  "requests",
  "FjoSpidie::Schema::Result::Request",
  { "foreign.entry_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 responses

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Response>

=cut

__PACKAGE__->has_many(
  "responses",
  "FjoSpidie::Schema::Result::Response",
  { "foreign.entry_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07035 @ 2013-03-29 12:01:28
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:eA40lf+9m5jkdamouEdVcA


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;
