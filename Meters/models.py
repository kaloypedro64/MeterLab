import datetime
from decimal import Decimal
from django.db import models
from datetime import date
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    suppliername = models.CharField(max_length=145)
    address = models.CharField(max_length=145, null=True)

    class Meta:
        db_table = "suppliers"


class brands(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=45, db_index=True)

    class Meta:
        db_table = "brands"


class mtype(models.Model):
    id = models.AutoField(primary_key=True)
    metertype = models.CharField(max_length=45, db_index=True)

    class Meta:
        db_table = "metertype"


class consumers(models.Model):
    id = models.AutoField(primary_key=True)
    consumer = models.CharField(max_length=145, null=True)
    address = models.CharField(max_length=145, null=True)
    type = models.CharField(max_length=2, null=True)
    active = models.PositiveSmallIntegerField(
        default=0, null=True)        # active, deleted

    class Meta:
        db_table = "consumers"


class acquisition(models.Model):
    id = models.AutoField(primary_key=True)
    transactiondate = models.DateField(("Date"), default=date.today)
    rrnumber = models.CharField(max_length=145, db_index=True)
    supplierid = models.ForeignKey(
        suppliers, db_column='supplierid', related_name='suppliers', on_delete=models.PROTECT, db_index=True)
    # units = models.IntegerField(default=0)
    area = models.PositiveSmallIntegerField(
        default=0, null=False)  # 0=dmo, 1=pas, 2=sas, 3=las
    userid = models.IntegerField(default=0)           # meter count
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    acqtype = models.PositiveSmallIntegerField(default=0, null=False)  # 0=meter, 1=seal

    class Meta:
        db_table = "acquisition"


class meters(models.Model):
    id = models.AutoField(primary_key=True)
    acquisitionid = models.ForeignKey(
        acquisition, db_column='acquisitionid', on_delete=models.PROTECT, db_index=True)
    brandid = models.ForeignKey(
        brands, db_column='brandid', on_delete=models.PROTECT, db_index=True)
    mtypeid = models.ForeignKey(
        mtype, db_column='mtypeid', on_delete=models.PROTECT, db_index=True)
    ampheres = models.CharField(max_length=45, null=True)
    serialnos = models.CharField(max_length=145, null=True)
    units = models.IntegerField(default=0)              # meter count
    class Meta:
        db_table = "meters"

class meterdetails(models.Model):
    id = models.AutoField(primary_key=True)
    meterid = models.ForeignKey(
        meters, db_column='meterid', on_delete=models.CASCADE, db_index=True)
    serialno = models.CharField(max_length=45, null=False)
    accuracy = models.CharField(max_length=45, null=True)
    wms_status = models.PositiveSmallIntegerField(
        default=0, null=True)    # 0=forwarded, 1=pending, 2=returned
    status = models.PositiveSmallIntegerField(
        default=0, null=True)    # Initial Testing, Transfer, Available, Installed, Damage/Salvage, Removed Meter, Calibration/Repair, for Verification
    # status = models.PositiveSmallIntegerField(
    #     default=0, null=True)    # pending, passed, failed
    active = models.PositiveSmallIntegerField(
        default=0, null=True)        # active, deleted

    class Meta:
        db_table = "meterdetails"


class seals(models.Model):
    id = models.AutoField(primary_key=True)
    acquisitionid = models.ForeignKey(
        acquisition, db_column='acquisitionid', on_delete=models.PROTECT, db_index=True)
    brandid = models.ForeignKey(
        brands, db_column='brandid', on_delete=models.PROTECT, db_index=True)
    boxes = models.IntegerField(default=0)
    ppb = models.IntegerField(default=0)              # pcs per box
    serialnos = models.CharField(max_length=45, null=True)

    @property
    def _get_total(self):
        return self.boxes * self.ppb
    total = property(_get_total)

    class Meta:
        db_table = "seals"


class sealdetails(models.Model):
    id = models.AutoField(primary_key=True)
    sealid = models.ForeignKey(
        seals, db_column='sealid', on_delete=models.CASCADE, db_index=True)
    meterdetailsid = models.ForeignKey(
        meterdetails, db_column='meterdetailsid', on_delete=models.PROTECT, db_index=True, null=True)
    serialno = models.CharField(max_length=45, null=False)
    techcrew = models.CharField(max_length=45, null=True)

    status = models.PositiveSmallIntegerField(
        default=0, null=True)
    active = models.PositiveSmallIntegerField(
        default=0, null=True)        # active, deleted

    class Meta:
        db_table = "sealdetails"



class metertest(models.Model):
    id = models.AutoField(primary_key=True)
    # consumersid = models.ForeignKey(
    #     consumers, db_column='consumers', on_delete=models.CASCADE, db_index=True)
    meterdetailsid = models.ForeignKey(
        meterdetails, db_column='consumersid', on_delete=models.CASCADE, db_index=True)
    testdate = models.DateField(("Date"), default=date.today)
    gen_average = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    fullload_average = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                           MinValueValidator(Decimal('0.00'))])
    lightload_average = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    fl1 = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                              MinValueValidator(Decimal('0.00'))])
    fl2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                              MinValueValidator(Decimal('0.00'))])
    fl3 = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                              MinValueValidator(Decimal('0.00'))])
    ll1 = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                              MinValueValidator(Decimal('0.00'))])
    ll2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                              MinValueValidator(Decimal('0.00'))])
    ll3 = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                              MinValueValidator(Decimal('0.00'))])
    reading = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    type = models.PositiveSmallIntegerField(
        default=0, null=True)        # type, class
    volts = models.CharField(max_length=45)
    phase = models.CharField(max_length=45)
    kh = models.CharField(max_length=45)
    ta = models.CharField(max_length=45)
    remarks = models.CharField(max_length=245)
    active = models.PositiveSmallIntegerField(
        default=0, null=True)        # active, deleted
    isdamage = models.BooleanField(default=False)
    userid = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "metertest"
        # abstract = True


class meterseal(models.Model):
    id = models.AutoField(primary_key=True)
    meterdetailsid = models.ForeignKey(
        meterdetails, db_column='meterdetailsid', on_delete=models.PROTECT, db_index=True)

    transactiondate = models.DateField(("Date"), default=date.today)
    seal_a = models.CharField(max_length=45, null=True)
    seal_b = models.CharField(max_length=45, null=True)
    metercondition = models.PositiveSmallIntegerField(
        default=0, null=True)        # good, damage, substandard, rehab
    accuracy = models.IntegerField(default=0)
    reading = models.IntegerField(default=0)
    remarks = models.CharField(max_length=245)

    active = models.PositiveSmallIntegerField(
        default=0, null=True)        # active, deleted

    userid = models.CharField(max_length=45)

    class Meta:
        db_table = "meterseal"


# class assigned_meter(models.Model):
#     id = models.AutoField(primary_key=True)
#     transactiondate = models.DateField(("Date"), default=date.today)
#     metertestid = models.ForeignKey(
#         metertest, db_column='metertestid', on_delete=models.PROTECT, db_index=True)
#     meterdetailsid = models.ForeignKey(
#         meterdetails, db_column='meterdetailsid', on_delete=models.PROTECT, db_index=True)
#     consumer = models.CharField(max_length=145, null=True)
#     address = models.CharField(max_length=145, null=True)
#     type = models.CharField(max_length=2, null=True)
#     active = models.PositiveSmallIntegerField(
#         default=0, null=True)        # active, deleted
#     userid = models.CharField(max_length=45)

#     class Meta:
#         db_table = "assigned_meter"





