export default function ({ $auth, redirect }) {
    const user = $auth.user
    console.log(user)
    if (user && user.u_type === 'tax_auditor') {
        // let the user in
    } else if (user && user.u_type === 'admin') {
        redirect('/admin/dashboard')

    } else if (user && user.u_type === 'seller') {
        redirect('/dashboard')
    }
}
