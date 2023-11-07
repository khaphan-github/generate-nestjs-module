import os
# Parent folder path
module_name = 'san_pham'
file_prefix = 'san_phan'
code_prefix = 'SanPham'

# Adjust the path as needed for your specific environment
parent_folder = f'{module_name}/'

# The array with the folder names to be created
structure_folders = ['commands', 'dto', 'events',
                     'migrations', 'model', 'proxy', 'queries', 'repositories', 'services']

# Creating each folder in the array
for folder in structure_folders:
    folder_path = os.path.join(parent_folder, folder)
    os.makedirs(folder_path, exist_ok=True)

# FILE PATH;
controler_file_path = parent_folder + file_prefix + '.controller.ts'
module_file_path = parent_folder + file_prefix + '.module.ts'
dto_file_path = parent_folder + 'dto/' + file_prefix + '.dto.ts'
service_file_path = parent_folder + 'services/' + file_prefix + '.service.ts'
repository_file_path = parent_folder + \
    'repositories/' + file_prefix + '.repository.ts'
# CREATE DTO FILES


# CREATE SINGLE FILE
controler_file_content = f"""
import {{   
    Body,
    Controller,
    Get,
    HttpCode,
    Post,
    Query,
    Request,
 }} from '@nestjs/common';
import {{ {code_prefix}Service }} from './services/{file_prefix}.service';
import {{ ApiOperation }} from '@nestjs/swagger';
import {{
  Search{code_prefix}DTO,
  Create{code_prefix}DTO,
  Update{code_prefix}DTO,
  Delete{code_prefix}DTO,
}} from './dto/{file_prefix}.dto';


@Controller('{file_prefix}')
export class {code_prefix}Controller {{
    contructor(private readonly service: {code_prefix}Service) {{}}

    @ApiOperation({{
        summary: 'Lấy thông tin một {code_prefix}',
        description: ``,
    }})
    @HttpCode(200)
    @Get('get-one/:id')
    public getOne{code_prefix}(@Param() id: string, @Request() req: any) {{
        const userId = req["user"].id;
        return this.service.getOne{code_prefix}(id , userId);
    }}

    @ApiOperation({{
        summary: 'Tìm kiếm / lọc {code_prefix}',
        description: ``,
    }})
    @HttpCode(200)
    @Get('search')
    public search{code_prefix}(@Body() body: Search{code_prefix}DTO, @Request() req: any) {{
        return this.service.search{code_prefix}();
    }}

    @ApiOperation({{
        summary: 'Tạo {code_prefix}',
        description: ``,
    }})
    @HttpCode(201)
    @Post('create')
    public async create{code_prefix}(@Body() body: Create{code_prefix}DTO, @Request() req: any) {{
        const userId = req["user"].id;
        return await this.service.create{code_prefix}(body, userId);
    }}

    @ApiOperation({{
        summary: 'Cập nhật {code_prefix}',
        description: ``,
    }})
    @HttpCode(200)
    @Post('update')
    public async update{code_prefix}(@Body() body: Update{code_prefix}DTO, @Request() req: any) {{
        const userId = req["user"].id;
        return await this.service.update{code_prefix}(body, userId);
    }}

    @ApiOperation({{
        summary: 'Xóa {code_prefix}',
        description: ``,
    }})
    @HttpCode(200)
    @Post('delete')
    public async delete{code_prefix}(@Body() body: Delete{code_prefix}DTO, @Request() req: any) {{
        const userId = req["user"].id;
        return await this.service.delete{code_prefix}(body, userId);
    }}
}}
    """

module_file_content = f"""
import {{ Module }} from '@nestjs/common';
import {{ CqrsModule }} from '@nestjs/cqrs';

import {{ QueryHandlers }} from './queries';
import {{ EventHandlers }} from './events';
import {{ CommandHandlers }} from './commands';

import {{ {code_prefix}Controller }} from './{file_prefix}.controller';
import {{ {code_prefix}Service }} from './services/{file_prefix}.service';
import {{ {code_prefix}Repository }} from './repositories/{file_prefix}.repository';

@Module({{
  imports: [
    PostgresModule.forFeature(DB),
    CqrsModule,
  ],
  controllers: [
    {code_prefix}Controller,
  ],
  providers: [
    ...QueryHandlers,
    ...CommandHandlers,
    ...EventHandlers,
    {code_prefix}Repository,
    {code_prefix}Service,
  ],
  exports: []
}})
export class {code_prefix}Module {{}}

"""

dto_file_content = f"""
import {{ ApiProperty }} from '@nestjs/swagger';

export class Create{code_prefix}DTO {{
    @ApiProperty({{ example: `Example` }})
    public example: number;
}}
export class Search{code_prefix}DTO {{
    @ApiProperty({{ example: `Example` }})
    public example: number;
}}

export class Update{code_prefix}DTO {{
    @ApiProperty({{ example: `Example` }})
    public example: number;
}}

export class Delete{code_prefix}DTO {{
    @ApiProperty({{ example: `Example` }})
    public example: number;
}}
"""

service_file_content = f"""

import {{ Injectable, Logger }} from '@nestjs/common';
import {{ CommandBus, QueryBus }} from '@nestjs/cqrs'
;
import {{ Create{code_prefix}Command }} from '../commands/create-{file_prefix}.command';
import {{ Update{code_prefix}Command }} from '../commands/update-{file_prefix}.command';
import {{ Delete{code_prefix}Command  }} from '../commands/delete-{file_prefix}.command';

import {{ GetAll{code_prefix}Query }} from '../queries/get-all-{file_prefix}.query'';
import {{ GetOne{code_prefix}Query }} from '../queries/get-one-{file_prefix}.query';
import {{ Search{code_prefix}Query }} from '../queries/search-{file_prefix}.query';

import {{
  Search{code_prefix}DTO,
  Create{code_prefix}DTO,
  Update{code_prefix}DTO,
  Delete{code_prefix}DTO,
}} from '../dto/{file_prefix}.dto';

@Injectable()
export class {code_prefix}Service {{
    private readonly logger = new Logger({code_prefix}Service.name);
    constructor(
        private readonly queryBus: QueryBus,
        private readonly commandBus: CommandBus,
    ) {{}}
  
    getOne{code_prefix}(id: string, userId: string) {{
        try {{
            return this.queryBus.execute(new GetOne{code_prefix}Query(id, userId))
        }} catch (err) {{
            this.logger.error(err);
        }}
    }}

    create{code_prefix}(dto: Create{code_prefix}DTO, userId: string) {{
        try {{
            return this.commandBus.execute(new Create{code_prefix}Command(body, userId))
        }} catch (err) {{
            this.logger.error(err);
        }}
    }}

    search{code_prefix}(dto: Search{code_prefix}DTO, userId: string) {{
        try {{
            return this.queryBus.execute(new Search{code_prefix}Query(dto, userId))
        }} catch (err) {{
            this.logger.error(err);
        }}
    }}

    update{code_prefix}(dto: Update{code_prefix}DTO, userId: string) {{
        try {{
            return this.commandBus.execute(new Update{code_prefix}Command(dto, userId))
        }} catch (err) {{
            this.logger.error(err);
        }}
    }}
    
    delete{code_prefix}(dto: Delete{code_prefix}DTO, userId: string) {{
        try {{
            return this.commandBus.execute(new Delete{code_prefix}Command(dto, userId))
        }} catch (err) {{
            this.logger.error(err);
        }}
    }}
}}

"""

repository_file_content = f"""
import {{ Injectable }} from '@nestjs/common';

@Injectable()
export class {code_prefix}Repository {{
    private readonly TABLE_NAME = 'change_table_name';
    constructor(
        @Connection(DB) private readonly pg: ConnectionPool,
    ) {{}}

    public getAll{code_prefix}() {{
        let params: any = [];
        const selectAttribute = ['*'];
        let queryText = `
            SELECT ${{selectAttribute.join(',')}}
            FROM ${{this.TABLE_NAME}}
        `;
        return this.pg.execute(queryText, params);
    }}

    public getOne{code_prefix}(options: any) {{
        const {{ id }} = options;
        const selectAttribute = ['*'];

        let params: any = [id];
        let queryText = `
            SELECT ${{selectAttribute.join(',')}}
            FROM ${{this.TABLE_NAME}}
            WHERE SOME_CONDITION
        `;
        return this.pg.execute(queryText, params);
    }}

    public getList{code_prefix}(options: any) {{
        const {{ id }} = options;
        let params: any = [];
        const selectAttribute = ['*'];
        let queryText = `
            SELECT ${{selectAttribute.join(',')}}
            FROM ${{this.TABLE_NAME}}
        `;
        return this.pg.execute(queryText, params);
    }}

    public search{code_prefix}(options: any, offset, limit: number) {{
        const {{ id }} = options;

        const params: any[] = [];
        const selectAttribute = ['*'];

        let queryText = `
            SELECT ${{selectAttribute.join(',')}}
            FROM ${{this.TABLE_NAME}}
            WHERE SOME_CONDITION
        `;

        // queryText += ` ORDER BY SOME_ATTRIBUTE ASC`; 
        if (limit) {{
            queryText += ` LIMIT $${{params.length + 1}}`;
            params.push(limit);
        }}

        if (offset) {{
            queryText += ` OFFSET $${{params.length + 1}}`;
            params.push(offset);
        }}

        return this.pg.execute(queryText, params);
    }}

    public update{code_prefix}(options: any) {{
        const {{ id, name }} = options;
        let params: any = [id, name];
        let queryText = `
            UPDATE ${{this.TABLE_NAME}}
            SET name = $2,
            WHERE id = $1
            RETURNING *
        `;
        return this.pg.execute(queryText, params);
    }}

    public create{code_prefix}(options: any) {{
        const {{ name }} = options;
        let params: any = [name];
        const tableAttributes = ['name', ];
        let queryText = `
            INSERT INTO ${{this.TABLE_NAME}}
            (${{tableAttributes.join(',')}})
            VALUES ($1)
            RETURNING *
        `;
        return this.pg.execute(queryText, params);
    }}

    public delete{code_prefix}(options: any) {{
        const {{ id }} = options;
        let params: any = [id];
        let queryText = `
            DELETE FROM ${{this.TABLE_NAME}}
            WHERE id = $1
        `;
        return this.pg.execute(queryText, params);
    }}
}}
"""

with open(controler_file_path, 'w',  encoding="utf-8") as file:
    file.write(controler_file_content)

with open(module_file_path, 'w',  encoding="utf-8") as file:
    file.write(module_file_content)

with open(dto_file_path, 'w',  encoding="utf-8") as file:
    file.write(dto_file_content)

with open(service_file_path, 'w',  encoding="utf-8") as file:
    file.write(service_file_content)

with open(repository_file_path, 'w',  encoding="utf-8") as file:
    file.write(repository_file_content)
# CREATE SINGLE FILE


# CREATE COMMANDS
command_index_file_path = parent_folder + 'commands/' + 'index.ts'
command_index_file_content = f"""
import {{ Update{code_prefix}CommandHandler }} from "./update-{file_prefix}.command";
import {{ Create{code_prefix}CommandHandler }} from "./create-{file_prefix}.command";
import {{ Delete{code_prefix}CommandHandler }} from "./delete-{file_prefix}.command";

export const CommandHandlers = [
    Update{code_prefix}CommandHandler,
    Create{code_prefix}CommandHandler,
    Delete{code_prefix}CommandHandler,
];

"""

create_command_file_path = parent_folder + \
    'commands/' + 'create-' + file_prefix + '.command.ts'
create_command_file_content = f"""

import {{ Logger }} from '@nestjs/common';
import {{ ICommand, ICommandHandler, CommandHandler }} from '@nestjs/cqrs';
import {{ {code_prefix}Repository }} from '../repositories/{file_prefix}.repository';

export class Create{code_prefix}Command implements ICommand {{
    constructor() {{}}
}}

@CommandHandler(Create{code_prefix}Command)
export class Create{code_prefix}CommandHandler
    implements ICommandHandler<Create{code_prefix}Command> {{
     private readonly logger = new Logger(Create{code_prefix}CommandHandler.name);

    constructor(
        private readonly repo: {code_prefix}Repository,
    ) {{}}

    async execute(
        command: Create{code_prefix}Command,
    ): Promise<any> {{
        const {{}} = command;
        const createData = {{}};
        return this.repo.create{code_prefix}(createData);
    }}
}}
"""

update_command_file_path = parent_folder + \
    'commands/' + 'update-' + file_prefix + '.command.ts'
update_command_file_content = f"""

import {{ Logger }} from '@nestjs/common';
import {{ ICommand, ICommandHandler, CommandHandler }} from '@nestjs/cqrs';
import {{ {code_prefix}Repository }} from '../repositories/{file_prefix}.repository';

export class Update{code_prefix}Command implements ICommand {{
    constructor() {{}}
}}

@CommandHandler(Update{code_prefix}Command)
export class Update{code_prefix}CommandHandler
    implements ICommandHandler<Update{code_prefix}Command> {{
     private readonly logger = new Logger(Update{code_prefix}CommandHandler.name);

    constructor(
        private readonly repo: {code_prefix}Repository,
    ) {{}}

    async execute(
        command: Update{code_prefix}Command,
    ): Promise<any> {{
        const {{}} = command;
        const updateData = {{}};
        return this.repo.update{code_prefix}(updateData);
    }}
}}
"""

delete_command_file_path = parent_folder + \
    'commands/' + 'delete-' + file_prefix + '.command.ts'

delete_command_file_content = f"""
import {{ Logger }} from '@nestjs/common';
import {{ ICommand, ICommandHandler, CommandHandler }} from '@nestjs/cqrs';
import {{ {code_prefix}Repository }} from '../repositories/{file_prefix}.repository';

export class Delete{code_prefix}Command implements ICommand {{
    constructor() {{}}
}}

@CommandHandler(Delete{code_prefix}Command)
export class Delete{code_prefix}CommandHandler
    implements ICommandHandler<Delete{code_prefix}Command> {{
     private readonly logger = new Logger(Delete{code_prefix}CommandHandler.name);

    constructor(
        private readonly repo: {code_prefix}Repository,
    ) {{}}

    async execute(
        command: Delete{code_prefix}Command,
    ): Promise<any> {{
        const {{}} = command;
        const deleteData = {{}};
        return this.repo.delete{code_prefix}(deleteData);
    }}
}}
"""

with open(command_index_file_path, 'w',  encoding="utf-8") as file:
    file.write(command_index_file_content)

with open(create_command_file_path, 'w',  encoding="utf-8") as file:
    file.write(create_command_file_content)

with open(update_command_file_path, 'w',  encoding="utf-8") as file:
    file.write(update_command_file_content)

with open(delete_command_file_path, 'w',  encoding="utf-8") as file:
    file.write(delete_command_file_content)

# CREATE COMMANDS


# CREATE QUERIES
query_index_file_path = parent_folder + 'queries/' + 'index.ts'
query_index_file_content = f"""
import {{ GetOne{code_prefix}QueryHandler }} from "./get-one-{file_prefix}.query";
import {{ GetAll{code_prefix}QueryHandler }} from "./get-all-{file_prefix}.query";
import {{ Search{code_prefix}QueryHandler }} from "./search-{file_prefix}.query";

export const QueryHandlers = [
    GetOne{code_prefix}QueryHandler,
    GetAll{code_prefix}QueryHandler,
    Search{code_prefix}QueryHandler,
];

"""

get_all_query_file_path = parent_folder + \
    'queries/' + 'get-all-' + file_prefix + '.query.ts'
get_all_query_file_content = f"""

import {{ Logger }} from '@nestjs/common';
import {{ IQuery, IQueryHandler, QueryHandler }} from '@nestjs/cqrs';
import {{ {code_prefix}Repository }} from '../repositories/{file_prefix}.repository';


export class GetAll{code_prefix}Query implements IQuery {{
    constructor() {{}}
}}

@QueryHandler(GetAll{code_prefix}Query)
export class GetAll{code_prefix}QueryHandler
    implements IQueryHandler<GetAll{code_prefix}Query> {{

    private readonly logger = new Logger(GetAll{code_prefix}QueryHandler.name);
    constructor(
        private readonly repo: {code_prefix}Repository,
    ) {{}}

    async execute(
        query: GetAll{code_prefix}Query,
    ): Promise<{code_prefix}[]> {{
        let result = await this.repo.GetAll(query)
        return result.rows.map(row => new {code_prefix}(row))
    }}
}}

"""

get_one_query_file_path = parent_folder + \
    'queries/' + 'get-one-' + file_prefix + '.query.ts'
get_one_query_file_content = f"""
import {{ Logger }} from '@nestjs/common';
import {{ IQuery, IQueryHandler, QueryHandler }} from '@nestjs/cqrs';
import {{ {code_prefix}Repository }} from '../repositories/{file_prefix}.repository';


export class GetOne{code_prefix}Query implements IQuery {{
    constructor() {{}}
}}

@QueryHandler(GetOne{code_prefix}Query)
export class GetOne{code_prefix}QueryHandler
    implements IQueryHandler<GetOne{code_prefix}Query> {{

    private readonly logger = new Logger(GetOne{code_prefix}QueryHandler.name);
    constructor(
        private readonly repo: {code_prefix}Repository,
    ) {{}}

    async execute(
        query: GetOne{code_prefix}Query,
    ): Promise<{code_prefix}[]> {{
        let result = await this.repo.GetOne(query)
        return result.rows.map(row => new {code_prefix}(row))
    }}
}}
"""

search_query_file_path = parent_folder + \
    'queries/' + 'search-' + file_prefix + '.query.ts'
search_query_file_content = f"""
import {{ Logger }} from '@nestjs/common';
import {{ IQuery, IQueryHandler, QueryHandler }} from '@nestjs/cqrs';
import {{ {code_prefix}Repository }} from '../repositories/{file_prefix}.repository';


export class Search{code_prefix}Query implements IQuery {{
    constructor() {{}}
}}

@QueryHandler(Search{code_prefix}Query)
export class Search{code_prefix}QueryHandler
    implements IQueryHandler<Search{code_prefix}Query> {{

    private readonly logger = new Logger(Search{code_prefix}QueryHandler.name);
    constructor(
        private readonly repo: {code_prefix}Repository,
    ) {{}}

    async execute(
        query: Search{code_prefix}Query,
    ): Promise<{code_prefix}[]> {{
        let result = await this.repo.Search(query)
        return result.rows.map(row => new {code_prefix}(row))
    }}
}}
132
"""

with open(query_index_file_path, 'w',  encoding="utf-8") as file:
    file.write(query_index_file_content)

with open(get_all_query_file_path, 'w',  encoding="utf-8") as file:
    file.write(get_all_query_file_content)

with open(get_one_query_file_path, 'w',  encoding="utf-8") as file:
    file.write(get_one_query_file_content)

with open(search_query_file_path, 'w',  encoding="utf-8") as file:
    file.write(search_query_file_content)

# CREATE QUERIES
