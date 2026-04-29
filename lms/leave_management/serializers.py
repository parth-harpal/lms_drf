from leave_management.models import LeaveType,LeaveBalance,LeaveRequest,LeaveLog
from user_mgmt.models import User
from rest_framework import serializers

# Leave Request Serializer for creating a leave request by employee
class LeaveRequestSerializer(serializers.ModelSerializer):
    '''
    Serializer for leave request
    '''
    leave_type_name=serializers.CharField(source='leave_type.name',read_only=True)
    employee_name=serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model=LeaveRequest
        fields=['id','employee_name','leave_type','leave_type_name','start_date','end_date','reason','applied_at','status','approved_by']
        read_only_fields=['applied_at','approved_by','employee_name','leave_type_name']

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError('Start date should be less than end date')
        return data

    

class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating a leave request 
    '''
    leave_type_name=serializers.CharField(source='leave_type.name',read_only=True)
    
    class Meta:
        model=LeaveRequest
        fields=['id','leave_type','leave_type_name','start_date','end_date','reason','status']
        read_only_fields=['status','leave_type_name','id']
    
    def create(self, validated_data):
        # If leave_type is a name string, find the LeaveType object
        leave_type = validated_data.get('leave_type')
        if isinstance(leave_type, str):
            leave_type = LeaveType.objects.get(name=leave_type)
            validated_data['leave_type'] = leave_type
        
        return super().create(validated_data)

class LeaveRequestUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for updating a leave request 
    '''
    class Meta:
        model=LeaveRequest
        fields=['start_date','end_date']

class LeaveRequestApproveSerializer(serializers.ModelSerializer):
    '''
    Serializer for approving and rejecting a leave request by manager
    '''
    class Meta:
        model=LeaveRequest
        fields=['status']

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveType
        fields=('id','name','max_leaves')

class LeaveBalanceSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.username',read_only=True)
    leave_type_name=serializers.CharField(source='leave_type.name',read_only=True)

    class Meta:
        model=LeaveBalance
        fields=('id','user_name','leave_type_name','total_leaves','used_leaves','remaining_leaves')

class LeaveLogSerializer(serializers.ModelSerializer):
    leave_request_name=serializers.CharField(source='leave_request.user.username',read_only=True)
    approved_by_name=serializers.CharField(source='approved_by.username',read_only=True)

    class Meta:
        model=LeaveLog
        fields=['id','leave_request','leave_request_name','action','approved_by_name']

