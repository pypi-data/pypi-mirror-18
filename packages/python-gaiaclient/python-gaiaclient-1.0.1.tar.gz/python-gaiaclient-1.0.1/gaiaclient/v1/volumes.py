"""Volume interface"""

from six.moves.urllib import parse

from gaiaclient.zeus.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('id', 'status', 'size', 'availability_zone', 'name',
                   'bootable', 'created_at', 'reference')
# Mapping of client keys to actual sort keys
SORT_KEY_MAPPINGS = {'name': 'name'}
# Additional sort keys for resources
SORT_KEY_ADD_VALUES = {
    'backups': ('data_timestamp', ),
    'messages': ('resource_type', 'event_id', 'resource_uuid',
                 'message_level', 'guaranteed_until', 'request_id'),
}


class Volume(base.Resource):
    """A volume is an extra block level storage to the OpenStack instances."""
    def __repr__(self):
        return "<Volume: %s>" % self.id

    def delete(self, cascade=False):
        """Delete this volume."""
        return self.manager.delete(self, cascade=cascade)

    def update(self, **kwargs):
        """Update the name or description for this volume."""
        return self.manager.update(self, **kwargs)

    def attach(self, instance_uuid, mountpoint, mode='rw', host_name=None):
        """Set attachment metadata.

        :param instance_uuid: uuid of the attaching instance.
        :param mountpoint: mountpoint on the attaching instance or host.
        :param mode: the access mode.
        :param host_name: name of the attaching host.
        """
        return self.manager.attach(self, instance_uuid, mountpoint, mode,
                                   host_name)

    def detach(self):
        """Clear attachment metadata."""
        return self.manager.detach(self)

    def reserve(self, volume):
        """Reserve this volume."""
        return self.manager.reserve(self)

    def unreserve(self, volume):
        """Unreserve this volume."""
        return self.manager.unreserve(self)

    def begin_detaching(self, volume):
        """Begin detaching volume."""
        return self.manager.begin_detaching(self)

    def roll_detaching(self, volume):
        """Roll detaching volume."""
        return self.manager.roll_detaching(self)

    def initialize_connection(self, volume, connector):
        """Initialize a volume connection.

        :param connector: connector dict from nova.
        """
        return self.manager.initialize_connection(self, connector)

    def terminate_connection(self, volume, connector):
        """Terminate a volume connection.

        :param connector: connector dict from nova.
        """
        return self.manager.terminate_connection(self, connector)

    def set_metadata(self, volume, metadata):
        """Set or Append metadata to a volume.

        :param volume : The :class: `Volume` to set metadata on
        :param metadata: A dict of key/value pairs to set
        """
        return self.manager.set_metadata(self, metadata)

    def set_image_metadata(self, volume, metadata):
        """Set a volume's image metadata.

        :param volume : The :class: `Volume` to set metadata on
        :param metadata: A dict of key/value pairs to set
        """
        return self.manager.set_image_metadata(self, volume, metadata)

    def delete_image_metadata(self, volume, keys):
        """Delete specified keys from volume's image metadata.

        :param volume: The :class:`Volume`.
        :param keys: A list of keys to be removed.
        """
        return self.manager.delete_image_metadata(self, volume, keys)

    def show_image_metadata(self, volume):
        """Show a volume's image metadata.

        :param volume : The :class: `Volume` where the image metadata
            associated.
        """
        return self.manager.show_image_metadata(self)

    def upload_to_image(self, force, image_name, container_format,
                        disk_format, visibility=None,
                        protected=None):
        """Upload a volume to image service as an image.
        :param force: Boolean to enables or disables upload of a volume that
                      is attached to an instance.
        :param image_name: The new image name.
        :param container_format: Container format type.
        :param disk_format: Disk format type.
        :param visibility: The accessibility of image (allowed for
                           3.1-latest).
        :param protected: Boolean to decide whether prevents image from being
                          deleted (allowed for 3.1-latest).
        """

        return self.manager.upload_to_image(self, force, image_name,
                                                container_format, disk_format)

    def force_delete(self):
        """Delete the specified volume ignoring its current state.

        :param volume: The UUID of the volume to force-delete.
        """
        return self.manager.force_delete(self)

    def reset_state(self, state, attach_status=None, migration_status=None):
        """Update the volume with the provided state.

        :param state: The state of the volume to set.
        :param attach_status: The attach_status of the volume to be set,
                              or None to keep the current status.
        :param migration_status: The migration_status of the volume to be set,
                                 or None to keep the current status.
        """
        return self.manager.reset_state(self, state, attach_status,
                                        migration_status)

    def extend(self, volume, new_size):
        """Extend the size of the specified volume.

        :param volume: The UUID of the volume to extend
        :param new_size: The desired size to extend volume to.
        """
        return self.manager.extend(self, new_size)

    def migrate_volume(self, host, force_host_copy, lock_volume):
        """Migrate the volume to a new host."""
        return self.manager.migrate_volume(self, host, force_host_copy,
                                           lock_volume)

    def retype(self, volume_type, policy):
        """Change a volume's type."""
        return self.manager.retype(self, volume_type, policy)

    def update_all_metadata(self, metadata):
        """Update all metadata of this volume."""
        return self.manager.update_all_metadata(self, metadata)

    def update_readonly_flag(self, volume, read_only):
        """Update the read-only access mode flag of the specified volume.

        :param volume: The UUID of the volume to update.
        :param read_only: The value to indicate whether to update volume to
            read-only access mode.
        """
        return self.manager.update_readonly_flag(self, read_only)

    def manage(self, host, ref, name=None, description=None,
               volume_type=None, availability_zone=None, metadata=None,
               bootable=False):
        """Manage an existing volume."""
        return self.manager.manage(host=host, ref=ref, name=name,
                                   description=description,
                                   volume_type=volume_type,
                                   availability_zone=availability_zone,
                                   metadata=metadata, bootable=bootable)

    def list_manageable(self, host, detailed=True, marker=None, limit=None,
                        offset=None, sort=None):
        return self.manager.list_manageable(host, detailed=detailed,
                                            marker=marker, limit=limit,
                                            offset=offset, sort=sort)

    def unmanage(self, volume):
        """Unmanage a volume."""
        return self.manager.unmanage(volume)

    def promote(self, volume):
        """Promote secondary to be primary in relationship."""
        return self.manager.promote(volume)

    def reenable(self, volume):
        """Sync the secondary volume with primary for a relationship."""
        return self.manager.reenable(volume)

    def get_pools(self, detail):
        """Show pool information for backends."""
        return self.manager.get_pools(detail)


class VolumeManager(base.ManagerWithDcId):
    """Manage :class:`Volume` resources."""
    resource_class = Volume

    def _build_list_url(self, resource_type, search_opts=None,
                        marker=None, limit=None, sort_key=None, sort_dir=None):

        if search_opts is None:
            search_opts = {}

        query_params = {}
        for key, val in search_opts.items():
            if val:
                query_params[key] = val

        if marker:
            query_params['marker'] = marker

        if limit:
            query_params['limit'] = limit

        if sort_key:
            query_params['sort_key'] = self._format_sort_key_param(
                sort_key,
                resource_type)

        if sort_dir:
            query_params['sort_dir'] = self._format_sort_dir_param(
                sort_dir)

        query_string = ""
        if query_params:
            params = sorted(query_params.items(), key=lambda x: x[0])
            query_string = "?%s" % parse.urlencode(params)

        return ("/v1/%(resource_type)s/%(query_string)s" %
                {"resource_type": resource_type,
                 "query_string": query_string})

    def _format_sort_param(self, sort, resource_type=None):
        '''Formats the sort information into the sort query string parameter.

        The input sort information can be any of the following:
        - Comma-separated string in the form of <key[:dir]>
        - List of strings in the form of <key[:dir]>
        - List of either string keys, or tuples of (key, dir)

        For example, the following import sort values are valid:
        - 'key1:dir1,key2,key3:dir3'
        - ['key1:dir1', 'key2', 'key3:dir3']
        - [('key1', 'dir1'), 'key2', ('key3', dir3')]

        :param sort: Input sort information
        :returns: Formatted query string parameter or None
        :raise ValueError: If an invalid sort direction or invalid sort key is
                           given
        '''
        if not sort:
            return None

        if isinstance(sort, six.string_types):
            # Convert the string into a list for consistent validation
            sort = [s for s in sort.split(',') if s]

        sort_array = []
        for sort_item in sort:
            if isinstance(sort_item, tuple):
                sort_key = sort_item[0]
                sort_dir = sort_item[1]
            else:
                sort_key, _sep, sort_dir = sort_item.partition(':')
            sort_key = sort_key.strip()
            sort_key = self._format_sort_key_param(sort_key, resource_type)
            if sort_dir:
                sort_dir = sort_dir.strip()
                if sort_dir not in SORT_DIR_VALUES:
                    msg = ('sort_dir must be one of the following: %s.'
                           % ', '.join(SORT_DIR_VALUES))
                    raise ValueError(msg)
                sort_array.append('%s:%s' % (sort_key, sort_dir))
            else:
                sort_array.append(sort_key)
        return ','.join(sort_array)

    def _format_sort_key_param(self, sort_key, resource_type=None):
        valid_sort_keys = SORT_KEY_VALUES
        if resource_type:
            add_sort_keys = SORT_KEY_ADD_VALUES.get(resource_type, None)
            if add_sort_keys:
                valid_sort_keys += add_sort_keys

        if sort_key in valid_sort_keys:
            return SORT_KEY_MAPPINGS.get(sort_key, sort_key)

        msg = ('sort_key must be one of the following: %s.' %
               ', '.join(valid_sort_keys))
        raise ValueError(msg)

    def _format_sort_dir_param(self, sort_dir):
        if sort_dir in SORT_DIR_VALUES:
            return sort_dir

        msg = ('sort_dir must be one of the following: %s.'
               % ', '.join(SORT_DIR_VALUES))
        raise ValueError(msg)

    def create(self, size, snapshot_id=None,
               name=None, description=None,
               volume_type=None, imageRef=None, scheduler_hints=None,
               ):
        """Create a volume.

        :param size: Size of volume in GB
        :param consistencygroup_id: ID of the consistencygroup
        :param group_id: ID of the group
        :param snapshot_id: ID of the snapshot
        :param name: Name of the volume
        :param description: Description of the volume
        :param volume_type: Type of volume
        :param user_id: User id derived from context
        :param project_id: Project id derived from context
        :param availability_zone: Availability Zone to use
        :param metadata: Optional metadata to set on volume creation
        :param imageRef: reference to an image stored in glance
        :param source_volid: ID of source volume to clone from
        :param source_replica: ID of source volume to clone replica
        :param scheduler_hints: (optional extension) arbitrary key-value pairs
                            specified by the client to help boot an instance
        :param multiattach: Allow the volume to be attached to more than
                            one instance
        :rtype: :class:`Volume`
         """

        body = {'volume': {'size': size,
                           'snapshot_id': snapshot_id,
                           'name': name,
                           'description': description,
                           'volume_type': volume_type,
                           'imageRef': imageRef
                           }}

        return self._create('/v1/volumes/', body, 'volume')

    def get(self, volume_id):
        """Get a volume.

        :param volume_id: The ID of the volume to get.
        :rtype: :class:`Volume`
        """
        return self._get("/v1/volumes/%s" % volume_id, "volume")

    def list(self, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, sort=None):
        """Lists all volumes.

        :param search_opts: Search options to filter out volumes.
        :param marker: Begin returning volumes that appear later in the volume
                       list than that represented by this volume id.
        :param limit: Maximum number of volumes to return.
        :param sort_key: Key to be sorted; deprecated in kilo
        :param sort_dir: Sort direction, should be 'desc' or 'asc'; deprecated
                         in kilo
        :param sort: Sort information
        :rtype: list of :class:`Volume`
        """

        resource_type = "volumes"
        url = self._build_list_url(resource_type,
                                   search_opts=search_opts, marker=marker,
                                   limit=limit, sort_key=sort_key,
                                   sort_dir=sort_dir)
        return self._list(url, resource_type)

    def delete(self, volume, cascade=False):
        """Delete a volume.

        :param volume: The :class:`Volume` to delete.
        :param cascade: Also delete dependent snapshots.
        """

        loc = "/v1/volumes/%s" % base.getid(volume)

        if cascade:
            loc += '?cascade=True'

        return self._delete(loc)

    def update(self, volume, **kwargs):
        """Update the name or description for a volume.

        :param volume: The :class:`Volume` to update.
        """
        if not kwargs:
            return

        body = {"volume": kwargs}

        return self._update("/v1/volumes/%s" % base.getid(volume), body)

    def _action(self, action, volume, info=None, **kwargs):
        """Perform a volume "action."
        """
        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/volumes/%s/action' % base.getid(volume)
        resp, body = self.api.client.post(url, body=body)
        return common_base.TupleWithMeta((resp, body), resp)

    def attach(self, volume, instance_uuid, mountpoint, mode='rw',
               host_name=None):
        """Set attachment metadata.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to attach.
        :param instance_uuid: uuid of the attaching instance.
        :param mountpoint: mountpoint on the attaching instance or host.
        :param mode: the access mode.
        :param host_name: name of the attaching host.
        """
        body = {'mountpoint': mountpoint, 'mode': mode}
        if instance_uuid is not None:
            body.update({'instance_uuid': instance_uuid})
        if host_name is not None:
            body.update({'host_name': host_name})
        return self._action('os-attach', volume, body)

    def detach(self, volume, attachment_uuid=None):
        """Clear attachment metadata.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to detach.
        :param attachment_uuid: The uuid of the volume attachment.
        """
        return self._action('os-detach', volume,
                            {'attachment_id': attachment_uuid})

    def reserve(self, volume):
        """Reserve this volume.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to reserve.
        """
        return self._action('os-reserve', volume)

    def unreserve(self, volume):
        """Unreserve this volume.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to unreserve.
        """
        return self._action('os-unreserve', volume)

    def begin_detaching(self, volume):
        """Begin detaching this volume.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to detach.
        """
        return self._action('os-begin_detaching', volume)

    def roll_detaching(self, volume):
        """Roll detaching this volume.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to roll detaching.
        """
        return self._action('os-roll_detaching', volume)

    def initialize_connection(self, volume, connector):
        """Initialize a volume connection.

        :param volume: The :class:`Volume` (or its ID).
        :param connector: connector dict from nova.
        """
        resp, body = self._action('os-initialize_connection', volume,
                                  {'connector': connector})
        return common_base.DictWithMeta(body['connection_info'], resp)

    def terminate_connection(self, volume, connector):
        """Terminate a volume connection.

        :param volume: The :class:`Volume` (or its ID).
        :param connector: connector dict from nova.
        """
        return self._action('os-terminate_connection', volume,
                            {'connector': connector})

    def set_metadata(self, volume, metadata):
        """Update/Set a volumes metadata.

        :param volume: The :class:`Volume`.
        :param metadata: A list of keys to be set.
        """
        body = {'metadata': metadata}
        return self._create("/volumes/%s/metadata" % base.getid(volume),
                            body, "metadata")

    def delete_metadata(self, volume, keys):
        """Delete specified keys from volumes metadata.

        :param volume: The :class:`Volume`.
        :param keys: A list of keys to be removed.
        """
        data = self._get("/volumes/%s/metadata" % base.getid(volume))
        metadata = data._info.get("metadata", {})
        if set(keys).issubset(metadata.keys()):
            for k in keys:
                metadata.pop(k)
            body = {'metadata': metadata}
            kwargs = {'headers': {'If-Match': data._checksum}}
            return self._update("/volumes/%s/metadata" % base.getid(volume),
                                body, **kwargs)

    def set_image_metadata(self, volume, metadata):
        """Set a volume's image metadata.

        :param volume: The :class:`Volume`.
        :param metadata: keys and the values to be set with.
        :type metadata: dict
        """
        return self._action("os-set_image_metadata", volume,
                            {'metadata': metadata})

    def delete_image_metadata(self, volume, keys):
        """Delete specified keys from volume's image metadata.

        :param volume: The :class:`Volume`.
        :param keys: A list of keys to be removed.
        """
        response_list = []
        for key in keys:
            resp, body = self._action("os-unset_image_metadata", volume,
                                      {'key': key})
            response_list.append(resp)

        return common_base.ListWithMeta([], response_list)

    def show_image_metadata(self, volume):
        """Show a volume's image metadata.

        :param volume : The :class: `Volume` where the image metadata
            associated.
        """
        return self._action("os-show_image_metadata", volume)

    def upload_to_image(self, volume, force, image_name, container_format,
                        disk_format, visibility, protected):
        """Upload volume to image service as image.

        :param volume: The :class:`Volume` to upload.
        """
        return self._action('os-volume_upload_image',
                            volume,
                            {'force': force,
                            'image_name': image_name,
                            'container_format': container_format,
                            'disk_format': disk_format,
                            'visibility': visibility,
                            'protected': protected})

    def force_delete(self, volume):
        """Delete the specified volume ignoring its current state.

        :param volume: The :class:`Volume` to force-delete.
        """
        return self._action('os-force_delete', base.getid(volume))

    def reset_state(self, volume, state, attach_status=None,
                    migration_status=None):
        """Update the provided volume with the provided state.

        :param volume: The :class:`Volume` to set the state.
        :param state: The state of the volume to be set.
        :param attach_status: The attach_status of the volume to be set,
                              or None to keep the current status.
        :param migration_status: The migration_status of the volume to be set,
                                 or None to keep the current status.
        """
        body = {'status': state} if state else {}
        if attach_status:
            body.update({'attach_status': attach_status})
        if migration_status:
            body.update({'migration_status': migration_status})
        return self._action('os-reset_status', volume, body)

    def extend(self, volume, new_size):
        """Extend the size of the specified volume.

        :param volume: The UUID of the volume to extend.
        :param new_size: The requested size to extend volume to.
        """
        return self._action('os-extend',
                            base.getid(volume),
                            {'new_size': new_size})

    def create_server_volume(self, server_id, volume_id, device=None):
        """
        Attach a volume identified by the volume ID to the given server ID

        :param server_id: The ID of the server
        :param volume_id: The ID of the volume to attach.
        :param device: The device name (optional)
        :rtype: :class:`Volume`
        """
        body = {'server-volume': {'volume_id': volume_id}}
        if device is not None:
            body['server-volume']['device'] = device
        return self._create("/v1/servers/%s/volumes" % server_id,
                            body, "server-volume")

    def get_server_volumes(self, server_id):
        """
        Get a list of all the attached volumes for the given server ID

        :param server_id: The ID of the server
        :rtype: list of :class:`Volume`
        """
        return self._list("/v1/servers/%s/volumes" % server_id,
                          "server-volumes")

    def delete_server_volume(self, server_id, volume_id):
        """
        Detach a volume identified by the attachment ID from the given server

        :param server_id: The ID of the server
        :param volume_id: The ID of the volume
        :returns: An instance of gaiaclient.common.base.TupleWithMeta
        """
        self._delete("/v1/servers/%s/volumes/%s" %
                            (server_id, volume_id))



