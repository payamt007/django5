import React, { useState } from 'react';
import { Divider, Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { DeleteTwoTone } from '@ant-design/icons'

interface DataType {
    key: React.Key;
    name: string;
    age: number;
    address: string;
}

const columns: ColumnsType<DataType> = [
    {
        title: 'Name',
        dataIndex: 'name',
        render: (text: string) => <a>{text}</a>,
    },
    {
        title: 'Age',
        dataIndex: 'age',
    },
    {
        title: 'Address',
        dataIndex: 'address',
    },
];

/* const data: DataType[] = [
    {
        key: '1',
        name: 'John Brown',
        age: 32,
        address: 'New York No. 1 Lake Park',
    },
    {
        key: '2',
        name: 'Jim Green',
        age: 42,
        address: 'London No. 1 Lake Park',
    },
    {
        key: '3',
        name: 'Joe Black',
        age: 32,
        address: 'Sydney No. 1 Lake Park',
    },
    {
        key: '4',
        name: 'Disabled User',
        age: 99,
        address: 'Sydney No. 1 Lake Park',
    },
]; */

// rowSelection object indicates the need for row selection


const Datatable: React.FC<{ data: DataType[] }> = ({data}) => {
    const rowSelection = {
        onChange: (selectedRowKeys: React.Key[], selectedRows: DataType[]) => {
            console.log(selectedRows.length)
            if (selectedRows.length > 0) {
                setdeleteButton(true)
            } else if (selectedRows.length == 0)
                setdeleteButton(false)

            console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
        },
        getCheckboxProps: (record: DataType) => ({
            disabled: record.name === 'Disabled User', // Column configuration not to be checked
            name: record.name,
        }),
    };

    const [deleteButton, setdeleteButton] = useState<boolean>(false);
    const handleDeletButtonClick = () => {
        console.log("clicked")
    }

    return (
        <div>
            {deleteButton ? <DeleteTwoTone onClick={handleDeletButtonClick} style={{ fontSize: '150%' }} /> : ''}

            <Divider />

            <Table
                rowSelection={{
                    ...rowSelection,
                }}
                columns={columns}
                dataSource={data}
            />
        </div>
    );
};

export default Datatable;