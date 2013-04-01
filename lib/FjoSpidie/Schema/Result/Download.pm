use utf8;
package FjoSpidie::Schema::Result::Download;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

FjoSpidie::Schema::Result::Download

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

=head1 TABLE: C<download>

=cut

__PACKAGE__->table("download");

=head1 ACCESSORS

=head2 id

  data_type: 'mediumint'
  is_auto_increment: 1
  is_nullable: 0

=head2 report_id

  data_type: 'mediumint'
  is_foreign_key: 1
  is_nullable: 0

=head2 data

  data_type: 'longblob'
  is_nullable: 1

=head2 md5

  data_type: 'blob'
  is_nullable: 1

=head2 sha1

  data_type: 'blob'
  is_nullable: 1

=head2 sha256

  data_type: 'blob'
  is_nullable: 1

=head2 filename

  data_type: 'blob'
  is_nullable: 1

=head2 size

  data_type: 'mediumtext'
  is_nullable: 1

=head2 uuid

  data_type: 'blob'
  is_nullable: 1

=cut

__PACKAGE__->add_columns(
  "id",
  { data_type => "mediumint", is_auto_increment => 1, is_nullable => 0 },
  "report_id",
  { data_type => "mediumint", is_foreign_key => 1, is_nullable => 0 },
  "data",
  { data_type => "longblob", is_nullable => 1 },
  "md5",
  { data_type => "blob", is_nullable => 1 },
  "sha1",
  { data_type => "blob", is_nullable => 1 },
  "sha256",
  { data_type => "blob", is_nullable => 1 },
  "filename",
  { data_type => "blob", is_nullable => 1 },
  "size",
  { data_type => "mediumtext", is_nullable => 1 },
  "uuid",
  { data_type => "blob", is_nullable => 1 },
);

=head1 PRIMARY KEY

=over 4

=item * L</id>

=back

=cut

__PACKAGE__->set_primary_key("id");

=head1 RELATIONS

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


# Created by DBIx::Class::Schema::Loader v0.07035 @ 2013-03-29 12:01:28
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:vR7/tufJlTDxXrh0OVNC+g


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;
