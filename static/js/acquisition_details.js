window.onload = function ()
{

    // select_brand(0);
    // select_mtypes(0);

    function loadMeters(params)
    {
        tablex = $('#tablex').DataTable({
            "searching": false,
            "info": false,
            "paging": true,
            "autoWidth": false,
            "columnDefs": [
                { "targets": [0], "searchable": false, "orderable": false, "visible": false },
                { "targets": [5], "width": "14%", "orderable": false, "visible": true },
                { "targets": [5], "className": 'text-right', },
            ],
            "keys": true,
            "keys": { "blurable": false },
            "select": true,
            "select": {
                "style": 'multi',
                "selector": 'td:first-child',
            },
            "serverSide": true,
            "processing": true,
            "ajax": function (data, callback, settings)
            {
                var sort_column_namex = data.columns[data.order[0].column].data.replace(/\./g, "__");
                var direction = "";
                if (data.order[0].dir == "desc") { direction = "-" };
                $.get(mListUrl, {
                    id: id,
                    limit: data.length,
                    start: data.start,
                    filter: data.search.value,
                    order_by: direction + sort_column_namex
                }, function (res)
                {
                    callback({
                        recordsTotal: res.length,
                        recordsFiltered: res.length,
                        data: res.objects
                    });
                });
            },
            columns: [
                { "data": "id" },
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        if ('{{ request.user.is_superuser }}' == 'True')
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick="edit_meter_modal(' + row["id"] + ')"><i class="fas fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick="meter_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                        else
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick="edit_meter_modal(' + row["id"] + ')"><i class="fal fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick="meter_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                    }
                },
                { "data": "brandid__brand" },
                { "data": "mtypeid__metertype" },
                { "data": "Amperes" },
                { "data": "units" },
                { "data": "serialnos" },
            ],
            // "dom": '<"top"i>rt<"bottom"flp><"clear">'
        });
        // tablex.column(0).visible(false);
    }
    loadMeters();

    function loadBrand()
    {

        table_brand = $('#table_brand').DataTable({
            "searching": false,
            "info": false,
            "paging": true,
            "autoWidth": false,
            "columnDefs": [
                { "targets": [0], "searchable": false, "orderable": false, "visible": false },
                { "targets": [1], "className": 'dt-body-left', "width": "20%", "orderable": false, "visible": true },
            ],
            "keys": true,
            "keys": { "blurable": false },
            "select": true,
            "select": {
                "style": 'multi',
                "selector": 'td:first-child',
            },
            "serverSide": true,
            "processing": true,
            "ajax": function (data, callback, settings)
            {
                var sort_column_namex = data.columns[data.order[0].column].data.replace(/\./g, "__");
                var direction = "";
                if (data.order[0].dir == "desc") { direction = "-" };
                $.get(brandssUrl, {
                    limit: data.length,
                    start: data.start,
                    filter: data.search.value,
                    order_by: direction + sort_column_namex
                }, function (res)
                {
                    callback({
                        recordsTotal: res.length,
                        recordsFiltered: res.length,
                        data: res.objects
                    });
                });
            },
            columns: [
                { "data": "id" },
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        if ('{{ request.user.is_superuser }}' == 'True')
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick="brand_edit(' + row["id"] + ')"><i class="fas fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick="brand_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                        else
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick="brand_edit(' + row["id"] + ')"><i class="fal fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick="brand_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                    }
                },
                { "data": "brand" },
            ],
            "dom": '<"top"i>rt<"bottom"flp><"clear">'
        });
        // table_brand.column(0).visible(false);
    }
    loadBrand();

    function loadmTypes()
    {
        table_types = $('#table_types').DataTable({
            "searching": false,
            "info": false,
            "paging": true,
            "autoWidth": false,
            "columnDefs": [
                { "targets": [0], "searchable": false, "orderable": false, "visible": false },
                { "targets": [1], "className": 'dt-body-left', "width": "20%", "orderable": false, "visible": true },
            ],
            "keys": true,
            "keys": { "blurable": false },
            "select": true,
            "select": {
                "style": 'multi',
                "selector": 'td:first-child',
            },
            "serverSide": true,
            "processing": true,
            "ajax": function (data, callback, settings)
            {
                var sort_column_namex = data.columns[data.order[0].column].data.replace(/\./g, "__");
                var direction = "";
                if (data.order[0].dir == "desc") { direction = "-" };
                $.get(mtypesssUrl, {
                    limit: data.length,
                    start: data.start,
                    filter: data.search.value,
                    order_by: direction + sort_column_namex
                }, function (res)
                {
                    callback({
                        recordsTotal: res.length,
                        recordsFiltered: res.length,
                        data: res.objects
                    });
                });
            },
            columns: [
                { "data": "id" },
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        if ('{{ request.user.is_superuser }}' == 'True')
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick="brand_edit(' + row["id"] + ')"><i class="fas fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick="mtypes_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                        else
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick="brand_edit(' + row["id"] + ')"><i class="fal fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick="mtypes_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                    }
                },
                { "data": "metertype" },
            ],
            "dom": '<"top"i>rt<"bottom"flp><"clear">'
        });
        table_types.column(0).visible(false);

    }
    loadmTypes();

    $('#tablex tbody').on('click', 'tr', function ()
    {
        $(this).toggleClass('selected');
    });
}

function add_meter_modal(params)
{
    $('#id_Amperes').editableSelect({ effects: 'fade' });
    $('#modal-add_meter').modal('show').draggable( { handle: ".modal-header" } );
}

function brand_modal(params)
{
    $('#modal-brand').modal('show').draggable({ handle: ".modal-header" });
}

function brand_save(params)
{
    var brand = $('#id_brand').val();
    $.ajax({
        url: brandsaveUrl,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { brand: brand, },
        success: function (data)
        {
            if (data.msg == 'saved')
            {
                Swal.fire('Successfully saved!', '', 'success');
                //Swal.fire('Successfully saved!', '', 'success')
                $('#table_brand').DataTable().ajax.reload(null, false);
            }
        },
        error: function (e)
        {
            Swal.fire('Error!', e, 'warning')
        }
    });
}

function brand_delete(params)
{
    var ok = confirm('Are you sure to delete this record?');
    if (ok == true)
    {
        $.ajax({
            url: branddelUrl,
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            contentType: false,
            data: { id: params, },
            success: function (data)
            {
                if (data.msg == 'deleted')
                {
                    Swal.fire('Successfully deleted!', '', 'success');
                    $('#table_brand').DataTable().ajax.reload(null, false);
                }
            },
            error: function (e)
            {
                Swal.fire('Error!', e, 'warning');
            }
        });
    }
}

function mtypes_modal(params)
{
    $('#modal-types').modal('show').draggable({ handle: ".modal-header" });
}

function mtypes_save(params)
{
    var metertype = $('#id_metertype').val();
    $.ajax({
        url: mtypessaveUrl,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { metertype: metertype, },
        success: function (data)
        {
            if (data.msg == 'saved')
            {
                Swal.fire('Successfully saved!', '', 'success');
                $('#table_types').DataTable().ajax.reload(null, false);
            }
        },
        error: function (e)
        {
            Swal.fire('Error!', e, 'warning');
        }
    });
}

function mtypes_delete(params)
{
    var ok = confirm('Are you sure to delete this record?');
    if (ok == true)
    {
        $.ajax({
            url: mtypesdelUrl,
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            contentType: false,
            data: { id: params, },
            success: function (data)
            {
                if (data.msg == 'deleted')
                {
                    Swal.fire('Successfully deleted!', '', 'success');
                    $('#table_types').DataTable().ajax.reload(null, false);
                }
            },
            error: function (e)
            {
                Swal.fire('Error!', e, 'warning');
            }
        });
    }
}

function meter_save(params)
{
    var acquisitionid = $('#id_id').val();
    var brandid = $('#id_brandid').val();
    var mtypeid = $('#id_mtypeid').val();
    var units = $('#id_units').val();
    var serialnos = $('#id_serialnos').val();
    var Amperes = $('#id_Amperes').val();

    // var csrf = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    $.ajax({
        url: mSaveUrl,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { acquisitionid: acquisitionid, units: units, serialnos: serialnos, brandid: brandid, mtypeid: mtypeid, Amperes: Amperes },
        // beforeSend: function (xhr)
        // {
        //     xhr.setRequestHeader("X-CSRFToken", csrf);
        // },
        success: function (data)
        {
            if (data.msg == 'saved')
            {
                $('#tablex').DataTable().ajax.reload(null, false);
                $('#modal-add_meter').modal('hide');
                Swal.fire('Successfully saved!', '', 'success');
            }
        },
        error: function (e)
        {
            Swal.fire('Error!', e, 'danger');
        }
    });
}

function edit_meter_modal(params)
{
    $.ajax({
        url: mEditUrl,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { option:"locate", id: params, },
        success: function (data)
        {

            $('#id_id_b').val(data.id);
            $("#id_brandid_b").select2().val(data.brandid).trigger('change.select2');
            $("#id_mtypeid_b").select2().val(data.mtypeid).trigger('change.select2');
            $('#id_units_b').val(data.units);
            $('#id_serialnos_b').val(data.serialnos);
            $('#id_Amperes_b').val(data.Amperes);
            $('#modal-edit_meter').modal('show').draggable({ handle: ".modal-header" });

        },
        error: function (e)
        {
            Swal.fire('Error!', e, 'warning');
        }
    });
}

function meter_update(params)
{
    var id = $('#id_id_b').val();
    var brandid = $('#id_brandid_b').val();
    var mtypeid = $('#id_mtypeid_b').val();
    var units = $('#id_units_b').val();
    var serialnos = $('#id_serialnos_b').val();
    var Amperes = $('#id_Amperes_b').val();
    $.ajax({
        url: mEditUrl,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { option:"update", id: id, brandid: brandid, mtypeid: mtypeid, Amperes: Amperes },
        success: function (data)
        {
            if (data.msg == 'updated')
            {
                $('#tablex').DataTable().ajax.reload(null, false);
                $('#modal-edit_meter').modal('hide');
                Swal.fire('Updated!', ' Successfully updated!', 'success');
            }
        },
        error: function (e)
        {
            Swal.fire('Error!', e, 'danger');
        }
    });
}

function meter_delete(params)
{
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        confirmButtonText: "Yes, delete it!",
        showCancelButton: true,
        cancelButtonColor: '#d33',
        icon: "question",
    }).then((result) =>
    {
        if (result.isConfirmed)
        {
            $.ajax({
                url: mDeleteUrl,
                type: 'GET',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                contentType: false,
                data: { id: params, },
                success: function (data)
                {
                    if (data.msg == 'deleted')
                    {
                        $('#tablex').DataTable().ajax.reload(null, false);
                        Swal.fire('Deleted!', ' Successfully deleted!', 'warning');
                    }
                },
                error: function (e)
                {
                    Swal.fire('Error!', e, 'warning');
                }
            });
        } else if (result.isDenied)
        {
            Swal.fire('Changes are not saved', '', 'error')
        }
    });
}

function select_brand(params)
{
    var e = document.getElementById("id_brandid");
    if (params == null)
        params = e.selectedIndex;
    var option = e.options[params];
    $('#id_brandid').val(option.value);
}

function select_mtypes(params)
{
    var e = document.getElementById("id_mtypeid");
    if (params == null)
        params = e.selectedIndex;
    var option = e.options[params];
    $('#id_mtypeid').val(option.value);
}
