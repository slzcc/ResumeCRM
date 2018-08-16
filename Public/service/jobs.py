table_config = [
            {
                'q': None,  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "选项",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "<input type='checkbox' />", 'kwargs': {}}, # 一个@符号表示取数据库内的数据，两个 @ 符号表示取全局变量中与自身相等的文本信息
                'attr': {}  # 自定义属性
            },            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}}, # 一个@符号表示取数据库内的数据，两个 @ 符号表示取全局变量中与自身相等的文本信息
                'attr': {}  # 自定义属性
            },
            {
                'q': 'department_demand__name',
                'title': "需求部门",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@department_demand__name'}},
                'attr': {}
            },            {
                'q': 'department_head__head',
                'title': "部门负责人",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@department_head__head'}},
                'attr': {}
            },
            # {
            #     'q': 'create_at',
            #     'title': "需求提交日期",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@create_at'}},
            #     'attr': {}
            # },
            # {
            #     'q': 'apply_information',
            #     'title': "应聘原因",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@apply_information'}},
            #     'attr': {}
            # },            {
            #     'q': 'customer_name__name',
            #     'title': "客户名称",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@customer_name__name'}},
            #     'attr': {}
            # },            {
            #     'q': 'customer_id__id',
            #     'title': "客户编号",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@customer_id__id'}},
            #     'attr': {}
            # },            {
            #     'q': 'projects_name__name',
            #     'title': "项目名称",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@projects_name__name'}},
            #     'attr': {}
            # },            {
            #     'q': 'projects_id__id',
            #     'title': "项目编号",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@projects_id__id'}},
            #     'attr': {}
            # },
            {
                'q': 'jobs',
                'title': "岗位名称",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@jobs'}},
                'attr': {
                    'edit-enable': 'true',
                    'edit-type': 'input'
                },
            },
            {
                'q': 'state',
                'title': "紧急程度",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@jobState_type_choices'}},
                'attr': {
                    'edit-enable': 'true',
                    'edit-type': 'select',
                    'global-name': "jobState_type_choices",
                    'origin': '@state'
                },
            },

            # {
            #     'q': 'personnel_type',
            #     'title': "正式人员",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@personnel_type'}},
            #     'attr': {}
            # },            {
            #     'q': 'personnel_attr',
            #     'title': "人员属性",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@personnel_attr'}},
            #     'attr': {}
            # },            {
            #     'q': 'customer_level__level',
            #     'title': "客户级别",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@customer_level__level'}},
            #     'attr': {}
            # },            {
            #     'q': 'onsite',
            #     'title': "Onsite",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@onsite'}},
            #     'attr': {}
            # },            {
            #     'q': 'on_business_trip',
            #     'title': "出差",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@on_business_trip'}},
            #     'attr': {}
            # },            {
            #     'q': 'degree',
            #     'title': "学历要求",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@degree'}},
            #     'attr': {}
            # },            {
            #     'q': 'work_time',
            #     'title': "工作年限",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@work_time'}},
            #     'attr': {}
            # },            {
            #     'q': 'equipped_computer',
            #     'title': "配备电脑",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@equipped_computer'}},
            #     'attr': {}
            # },            {
            #     'q': 'personnel_costs',
            #     'title': "人员成本类型",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@personnel_costs'}},
            #     'attr': {}
            # },
            {
                'q': 'number',
                'title': "需求人数",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@number'}},
                'attr': {
                    'name': 'number',
                    'edit-enable': 'true',
                    'edit-type': 'input'
                },
            },
            {
                'q': 'work_place__name',
                'title': "工作地点",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@work_place__name'}},
                'attr': {
                        'name': "work_place_name",
                        "edit-enable": "true",
                        'edit-type': 'select',
                        'global-name': "work_place_choices",
                        'origin': '@work_place__id'
                        },
            },
            {
                'q': 'work_place__id',
                'title': "",
                'display': 2,
                'text': {},
                'attr': {},
            },
            # {
            #     'q': 'salary',
            #     'title': "薪资范围",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@salary'}},
            #     'attr': {}
            # },            {
            #     'q': 'position_requirements',
            #     'title': "岗位需求信息",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@position_requirements'}},
            #     'attr': {}
            # },            {
            #     'q': 'search_key',
            #     'title': "岗位关键字",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@search_key'}},
            #     'attr': {}
            # },            {
            #     'q': 'joblevel',
            #     'title': "岗位级别",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@joblevel'}},
            #     'attr': {}
            # },            {
            #     'q': 'jobs_highlight',
            #     'title': "岗位亮点",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@jobs_highlight'}},
            #     'attr': {}
            # },            {
            #     'q': 'project_size',
            #     'title': "岗位规模",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@project_size'}},
            #     'attr': {}
            # },            {
            #     'q': 'referral_bonus',
            #     'title': "推荐奖金",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@referral_bonus'}},
            #     'attr': {}
            # },            {
            #     'q': 'customers',
            #     'title': "客户介绍",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@customers'}},
            #     'attr': {}
            # },            {
            #     'q': 'describe',
            #     'title': "备注",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@describe'}},
            #     'attr': {}
            # },
            {
                'q': 'candidate__username',
                'title': "候选人",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@candidate__username'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': '''<td class="actions">
	<a href="#" class="on-default edit-row" data-toggle="tooltip" data-placement="top" title="" data-original-title="Edit"><i class="fa fa-pencil"></i></a>
	<a href="#" class="on-default remove-row" data-toggle="tooltip" data-placement="top" title="" data-original-title="Delete"><i class="fa fa-trash-o"></i></a>
	<a href="#" class="hidden on-editing save-row" data-toggle="tooltip" data-placement="top" title="" data-original-title="Save"><i class="fa fa-save"></i></a>
	<a href="#" class="hidden on-editing cancel-row" data-toggle="tooltip" data-placement="top" title="" data-original-title="Cancel"><i class="fa fa-times"></i></a>
</td>''',
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]