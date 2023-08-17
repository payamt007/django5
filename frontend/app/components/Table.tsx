import React, { useState } from 'react';
import { Divider, Table, Space, Input, InputNumber, Form, Typography, Popconfirm, Checkbox } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { DeleteTwoTone, PlusCircleTwoTone, CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons'
import { feedType } from '@/lib/types/feeds';
import { useForm } from 'react-hook-form';
import { useCreateFeedMutation, useUpdateFeedMutation } from "@/lib/services/feed"

interface EditableCellProps extends React.HTMLAttributes<HTMLElement> {
    editing: boolean;
    dataIndex: string;
    title: any;
    inputType: 'number' | 'text' | 'checkbox';
    record: feedType;
    index: number;
    children: React.ReactNode;
}



const Datatable: React.FC<{ dataSource: feedType[] }> = ({ dataSource }) => {

    const [createFeed, { isLoading, isError, error }] = useCreateFeedMutation()
    const [updateFeed] = useUpdateFeedMutation()

    const [form] = Form.useForm();
    const [editingKey, setEditingKey] = useState('');

    const EditableCell: React.FC<EditableCellProps> = ({
        editing,
        dataIndex,
        title,
        inputType,
        record,
        index,
        children,
        ...restProps
    }) => {
        //const inputNode = inputType === 'checkbox' ? <Checkbox /> : <Input />;
        const inputNodeCalculator = (inputType: string) => {
            if (inputType === 'checkbox') {
                return <Checkbox checked={form.getFieldValue(dataIndex)} />
            }
            else if (inputType === 'number')
                return <InputNumber />
            else
                return <Input />
        }
        const inputNode = inputNodeCalculator(inputType)

        const handleCheckboxChange = (e) => {
            const { name, checked } = e.target;
            console.log("name, checked", name, checked)
            form.setFieldsValue({ [name]: checked });
            //console.log(form)
        };

        return (
            <td {...restProps}>
                {editing ? (
                    <Form.Item
                        name={dataIndex}
                        style={{ margin: 0 }}
                        trigger="onChange"
                    >
                        {inputType === 'checkbox' ? (
                            <Checkbox
                                name={dataIndex}
                                //checked={record[dataIndex]}
                                checked={form.getFieldValue(dataIndex)}
                                onChange={handleCheckboxChange}
                            />
                        ) : (
                            inputNode
                        )}
                    </Form.Item>
                ) : (
                    children
                )}
            </td>
        );
    };

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            editable: false,

        },
        {
            title: 'Title',
            dataIndex: 'title',
            editable: true,

        },
        {
            title: 'Link',
            dataIndex: 'link',
            editable: true,
        },
        {
            title: 'Followed',
            dataIndex: 'followed',
            render: (followed: boolean) => (followed ? <CheckCircleTwoTone /> : <CloseCircleTwoTone twoToneColor="#eb2f96" />),
            editable: true,
        },
        {
            title: 'Stopped',
            dataIndex: 'stopped',
            render: (stopped: boolean) => (stopped ? <CheckCircleTwoTone /> : <CloseCircleTwoTone twoToneColor="#eb2f96" />),
            editable: true,
        },
        {
            title: 'Fails',
            dataIndex: 'fails',
            render: (fails: number) => (fails ? fails : 0),
            editable: false,
        },
        {
            title: 'operation',
            dataIndex: 'operation',
            render: (_: any, record: feedType) => {
                const editable = isEditing(record);
                return editable ? (
                    <span>
                        <Typography.Link onClick={() => save(record.id)} style={{ marginRight: 8 }}>
                            Save
                        </Typography.Link>
                        <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
                            <a>Cancel</a>
                        </Popconfirm>
                    </span>
                ) : (
                    <Typography.Link disabled={editingKey !== ''} onClick={() => edit(record)}>
                        Edit
                    </Typography.Link>
                );
            },
        },
    ];

    const edit = (record: Partial<feedType> & { key: React.Key }) => {
        console.log("start editing")
        form.setFieldsValue({
            ...record,
            followed: record.followed,
            stopped: record.stopped,
        });
        setEditingKey(record.key);
    };

    const cellTypeDetector = (index: string): string => {
        if (index == "stopped")
            return "checkbox"
        else if (index == "followed")
            return "checkbox"
        else
            return "text"

    }

    const mergedColumns = columns.map((col) => {
        if (!col.editable) {
            return col;
        }
        return {
            ...col,
            onCell: (record: feedType) => ({
                record,
                inputType: cellTypeDetector(col.dataIndex),
                dataIndex: col.dataIndex,
                title: col.title,
                editing: isEditing(record),
            }),
        };
    });

    const isEditing = (record: feedType) => record.id === parseInt(editingKey);

    const rowSelection = {
        onChange: (selectedRowKeys: React.Key[], selectedRows: feedType[]) => {
            console.log(selectedRows.length)
            if (selectedRows.length > 0) {
                setdeleteButton(true)
            } else if (selectedRows.length == 0)
                setdeleteButton(false)

            console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
        },
        /* getCheckboxProps: (record: feedType) => ({
            disabled: record.name === 'Disabled User', // Column configuration not to be checked
            name: record.name,
        }), */
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

    const cancel = () => {
        setEditingKey('');
    };

    const save = async (key: React.Key) => {

        try {
            //console.log(form)
            const row = (await form.getFieldsValue()) as feedType;
            //form.getFieldsValue
            let updatePaylod = row
            updatePaylod.id = key
            console.log(updatePaylod)
            await updateFeed(row)
            setEditingKey('');
        } catch (errInfo) {
            console.log('Validate Failed:', errInfo);
        }
    };

    return (
        <Form form={form} component={false}>
            <div>
                {deleteButton ? <DeleteTwoTone onClick={handleDeletButtonClick} style={{ fontSize: '150%' }} /> : ''}
                <Divider />
                <Table
                    components={{
                        body: {
                            cell: EditableCell,
                        },
                    }}
                    rowSelection={{
                        ...rowSelection,
                    }}
                    columns={mergedColumns}
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
        </Form>
    );
};

export default Datatable;