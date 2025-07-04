import z from 'zod'

export const schema = z.object({
  username: z
    .string()
    .min(1, { message: 'Required*' })
    .min(3, { message: 'Username must be at least 3 characters long' })
    .max(25, { message: 'Username must be at most 25 characters long' })
    .regex(/^[a-zA-Z0-9_]+$/, {
      message: 'Username can only contain letters, numbers, and underscores'
    })
    .regex(/^\S+$/, { message: 'Username must not contain spaces' }),
  password: z
    .string()
    .min(1, { message: 'Required*' })
    .min(6, { message: 'Password must be at least 6 characters long' })
    .max(100, { message: 'Password must be at most 100 characters long' })
    .regex(/(?=.*[a-z])/, { message: 'Password must contain at least one lowercase letter' })
    .regex(/(?=.*[A-Z])/, { message: 'Password must contain at least one uppercase letter' })
    .regex(/(?=.*\d)/, { message: 'Password must contain at least one number' })
})
