import React, { useState } from 'react';
import { Divider, Table, Space, Input } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { DeleteTwoTone, PlusCircleTwoTone, CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons'
import { feedType } from '@/lib/types/feeds';
import { useForm } from 'react-hook-form';
import { useCreateFeedMutation } from "@/lib/services/feed"

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
        render: (followed: boolean) => (followed ? <CheckCircleTwoTone /> : <CloseCircleTwoTone twoToneColor="#eb2f96" />),
    },
    {
        title: 'Stopped',
        dataIndex: 'stopped',
        render: (followed: boolean) => (followed ? <CheckCircleTwoTone /> : <CloseCircleTwoTone twoToneColor="#eb2f96" />),
    },
    {
        title: 'Fails',
        dataIndex: 'fails',
        render: (followed: boolean) => (followed ? <CheckCircleTwoTone /> : 0),
    },
];

const Datatable: React.FC<{ dataSource: feedType[] }> = ({ dataSource }) => {

    const [createFeed, { isLoading, isError, error }] = useCreateFeedMutation()

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
    const handleDeletButtonClick = () => {
        console.log("clicked")
    }
    const handleAddFeed = async (data) => {
        await createFeed(data)
        console.log(data)
    }

    const { register, handleSubmit, formState: { errors }, } = useForm();

    return (
        <div>
            {deleteButton ? <DeleteTwoTone onClick={handleDeletButtonClick} style={{ fontSize: '150%' }} /> : ''}
            <Divider />
            <Table
                rowSelection={{
                    ...rowSelection,
                }}
                columns={columns}
                dataSource={dataSource}
            />
            <div>
                <PlusCircleTwoTone onClick={handleAddFeed} style={{ fontSize: '150%' }} />
            </div>
            <form onSubmit={handleSubmit(handleAddFeed)}>
                <input {...register('title', { required: true })} />
                {errors.title && <p>Title is required.</p>}
                <input {...register('link', { required: true })} />
                {errors.link && <p>Link is required.</p>}
                <input type="submit" value={'submit'} />
            </form>
        </div>
    );
};

export default Datatable;