
window.onload = function ()
{
    function loadMeters(params)
    {
        tablex = $('#tablex').DataTable({
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
                $.get(mListUrl, {
                    id:id,
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
                { "data": "brandid__brand" },
                { "data": "mtypeid__metertype" },
                { "data": "units" },
                { "data": "serialnos" },
            ],
            "dom": '<"top"i>rt<"bottom"flp><"clear">'
        });
        // tablex.column(0).visible(false);
    }
    loadMeters();

    // select_supplier(0);

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
                msgAlert('Save', 'Successfully saved!', 1);
                $('#table_brand').DataTable().ajax.reload(null, false);
            }
        },
        error: function (e)
        {
            alert('err: brand_save');
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
                    msgAlert('Delete', 'Successfully deleted!', 3);
                    $('#table_brand').DataTable().ajax.reload(null, false);
                }
            },
            error: function (e)
            {
                alert('err: brand_save');
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
                msgAlert('Save', 'Successfully saved!', 1);
                $('#table_types').DataTable().ajax.reload(null, false);
            }
        },
        error: function (e)
        {
            alert('err: brand_save');
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
                    msgAlert('Delete', 'Successfully deleted!', 3);
                    $('#table_types').DataTable().ajax.reload(null, false);
                }
            },
            error: function (e)
            {
                alert('err: brand_save');
            }
        });
    }
}

// function meter_to_datatable(params)
// {
//     if ($('#id_serialnos').val() == '')
//     {
//         $('#id_serialnos').focus();
//         return;
//     }
//     if ($('#id_units').val() == '')
//     {
//         $('#id_units').focus();
//         return;
//     }
//     tablex.row.add([
//         0,
//         $("#id_brandid option:selected").text(),
//         $("#id_mtypeid option:selected").text(),
//         $('#id_units').val(),
//         $('#id_serialnos').val(),
//         $('#id_brandid').val(),
//         $('#id_mtypeid').val(),
//     ]).draw(false);
// }

function meter_save(params)
{

    var acquisitionid = $('#id_id').val();
    var units = $('#id_units').val();
    var serialnos = $('#id_serialnos').val();
    var brandid = $('#id_brandid').val();
    var mtypeid = $('#id_mtypeid').val();
    var ampheres = $('#id_mtypeid').val();
    var csrf = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    $.ajax({
        url: mSaveUrl,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { acquisitionid: acquisitionid, units: units, serialnos: serialnos, brandid: brandid, mtypeid: mtypeid, ampheres: ampheres },
        beforeSend: function (xhr)
        {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
        success: function (data)
        {
            alert(data.msg);
            // if (data.msg == 'deleted')
            // {
            //     msgAlert('Delete', 'Successfully deleted!', 3);
            //     $('#table_types').DataTable().ajax.reload(null, false);
            // }
        },
        error: function (e)
        {
            alert('err: brand_save');
        }
    });
}
