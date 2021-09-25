window.onload = function ()
{
    $('.select2').select2();
    // $('#id_brand').editableSelect({ effects: 'fade' });
    // $('#id_metertype').editableSelect({ effects: 'fade' });
    // $('#id_ampheres').editableSelect({ effects: 'fade' });
    // $('#id_ampheres').editableSelect({ effects: 'fade' });

    tablex = $('#tablex').DataTable({
        // "scrollX": true,
        "searching": false,
        "processing": true,
        "info": false,
        'autoWidth': false,
        // "paging": true,
        "lengthChange": false,
        // "responsive": true,
        // "order": [1, "asc"],
        "columnDefs": [
            { "targets": [4], "className": "text-right" },
            { "targets": [0,5,6], "visible": false },
        ],

    });
    // tablex.column(0).visible(false);
    // tablex.column(5).visible(false);
    // tablex.column(6).visible(false);

    select_supplier(0);

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
        table_brand.column(0).visible(false);

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

function meter_to_datatable(params)
{
    if ($('#id_serialnos').val() == '')
    {
        $('#id_serialnos').focus();
        return;
    }
    if ($('#id_units').val() == '')
    {
        $('#id_units').focus();
        return;
    }
    tablex.row.add([
        0,
        $("#id_brandid option:selected").text(),
        $("#id_mtypeid option:selected").text(),
        $('#id_units').val(),
        $('#id_serialnos').val(),
        $('#id_brandid').val(),
        $('#id_mtypeid').val(),
    ]).draw(false);
}

function select_supplier(params)
{
    var e = document.getElementById("id_supplier");
    if (params == null) params = e.selectedIndex
    var option = e.options[params];
    // var attrs = option.attributes;
    var data = option.getAttribute("data-address");
    $('#id_supplierid').val(option.value);
    document.getElementById('lblAddress').innerHTML = data;
}