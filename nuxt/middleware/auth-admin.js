export default async function({ $auth, redirect }) {
  let user = $auth.user
  if (user && user.role == 'admin') {
    // let the user in
  } else {
    redirect('/dashboard')
  }
}
