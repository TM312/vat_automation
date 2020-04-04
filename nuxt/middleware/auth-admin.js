export default function ({ $auth, redirect }) {
  const user = $auth.user
  if (user && user.role === 'admin') {
    // let the user in
  } else {
    redirect('/dashboard')
  }
}
