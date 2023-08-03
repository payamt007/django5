import React, { useState } from 'react';
import { Divider, Table,Space, Input } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { DeleteTwoTone, PlusCircleTwoTone } from '@ant-design/icons'
import { feedType  } from '@/lib/types/feeds';


const columns: ColumnsType<feedType> = [
    {
        title: 'Title',
        dataIndex: 'title',
    },
    {
        title: 'Link',
        dataIndex: 'link',
    },
    {
        title: 'Followed',
        dataIndex: 'followed',
    },
    {
        title: 'Stopped',
        dataIndex: 'stopped',
    },
    {
        title: 'Fails',
        dataIndex: 'fails',
    },
];

const Datatable: React.FC<{ data: feedType[] }> = ({ data }) => {

    const rowSelection = {
        onChange: (selectedRowKeys: React.Key[], selectedRows: feedType[]) => {
            console.log(selectedRows.length)
            if (selectedRows.length > 0) {
                setdeleteButton(true)
            } else if (selectedRows.length == 0)
                setdeleteButton(false)

            console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
        },
        getCheckboxProps: (record: feedType) => ({
            disabled: record.name === 'Disabled User', // Column configuration not to be checked
            name: record.name,
        }),
    };

    const [deleteButton, setdeleteButton] = useState<boolean>(false);
    const [newLink, setnewLink] = useState<string>("");
    const [newTitle, setnewTitle] = useState<string>("");
    const handleDeletButtonClick = () => {
        console.log("clicked")
    }
    const handleAddFeed = () => {
        console.log("clicked add")
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
            <div>
                <PlusCircleTwoTone onClick={handleAddFeed} style={{ fontSize: '150%' }} />
            </div>
            <Space.Compact>
                <Input placeholder='Enter the title of feed' />
                <br/>
                <Input placeholder='Input The link of feed' />
                <PlusCircleTwoTone />
            </Space.Compact>
        </div>
    );
};

export default Datatable;