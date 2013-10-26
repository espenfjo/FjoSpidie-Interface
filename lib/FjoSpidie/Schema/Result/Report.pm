use utf8;
package FjoSpidie::Schema::Result::Report;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

FjoSpidie::Schema::Result::Report

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

=head1 TABLE: C<report>

=cut

__PACKAGE__->table("report");

=head1 ACCESSORS

=head2 id

  data_type: 'mediumint'
  is_auto_increment: 1
  is_nullable: 0

=head2 url

  data_type: 'blob'
  is_nullable: 1

=head2 starttime

  data_type: 'timestamp'
  datetime_undef_if_invalid: 1
  default_value: '0000-00-00 00:00:00'
  is_nullable: 0

=head2 endtime

  data_type: 'timestamp'
  datetime_undef_if_invalid: 1
  default_value: '0000-00-00 00:00:00'
  is_nullable: 0

=head2 uuid

  data_type: 'varchar'
  is_nullable: 1
  size: 36

=cut

__PACKAGE__->add_columns(
  "id",
  { data_type => "mediumint", is_auto_increment => 1, is_nullable => 0 },
  "url",
  { data_type => "blob", is_nullable => 1 },
  "starttime",
  {
    data_type => "timestamp",
    datetime_undef_if_invalid => 1,
    default_value => "0000-00-00 00:00:00",
    is_nullable => 0,
  },
  "endtime",
  {
    data_type => "timestamp",
    datetime_undef_if_invalid => 1,
    default_value => "0000-00-00 00:00:00",
    is_nullable => 0,
  },
  "uuid",
  { data_type => "varchar", is_nullable => 1, size => 36 },
);

=head1 PRIMARY KEY

=over 4

=item * L</id>

=back

=cut

__PACKAGE__->set_primary_key("id");

=head1 RELATIONS

=head2 alerts

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Alert>

=cut

__PACKAGE__->has_many(
  "alerts",
  "FjoSpidie::Schema::Result::Alert",
  { "foreign.report_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 downloads

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Download>

=cut

__PACKAGE__->has_many(
  "downloads",
  "FjoSpidie::Schema::Result::Download",
  { "foreign.report_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 entries

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Entry>

=cut

__PACKAGE__->has_many(
  "entries",
  "FjoSpidie::Schema::Result::Entry",
  { "foreign.report_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 graphs

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Graph>

=cut

__PACKAGE__->has_many(
  "graphs",
  "FjoSpidie::Schema::Result::Graph",
  { "foreign.report_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 pcaps

Type: has_many

Related object: L<FjoSpidie::Schema::Result::Pcap>

=cut

__PACKAGE__->has_many(
  "pcaps",
  "FjoSpidie::Schema::Result::Pcap",
  { "foreign.report_id" => "self.id" },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07035 @ 2013-07-12 16:57:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:XZFWMvVP9c1dkMQYxH1x6A


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;
