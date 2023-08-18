import { useForm, SubmitHandler } from "react-hook-form"


type Inputs = {
  title: string
  linke: string
}


export default function CreatForm({ submitToServerFunc }) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Inputs>()
  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    console.log(data)
   await submitToServerFunc(data)
  }

  console.log(watch("example"))


  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input defaultValue="test" {...register("example")} />
      <input {...register("exampleRequired", { required: true })} />
      {errors.exampleRequired && <span>This field is required</span>}
      <input type="submit" />
    </form>
  )
}