from typed.func import service, action
from utils.path import File
from runtime.mods.env.err import EnvErr

@service(err=EnvErr)
class env:
    @typed
    def all(envpath: Maybe(Path)=None) -> Dict:
        if not envpath:
            envpath = env.dotenv()
            if not envpath:
                envpath = '.env'
        if not path.exists(envpath):
            raise EnvErr(f".env file not found at '{envpath}'.")
        with open(envpath, 'r') as f:
            env_ = {}
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                equals_index = line.find('=')
                if equals_index == -1:
                    continue
                key = line[:equals_index].strip()
                value = line[equals_index + 1:].strip()
                env_.update({key: value})
            return env_

    @typed
    def environ() -> Dict:
        try:
            return os.environ
        except Exception as e:
            raise EnvErr(e)

    @typed
    def print(envpath: Maybe(Path)=None) -> Nill:
        print(env.get_all(envpath))

    @typed
    def get(env: Env='') -> Any:
        if not env.is_defined(env):
            raise EnvErr(f"The env '{env}' is not defined.")
        value = os.getenv(env)
        try:
            processed_value = value.replace("'", '"')
            parsed_value = json.loads(processed_value)
            if isinstance(parsed_value, (list, dict)) or (isinstance(parsed_value, (int, float, bool)) and not value.isdigit() and not (value.count('.') == 1 and value.replace('.', '').isdigit())):
                return parsed_value
            elif isinstance(parsed_value, str) and parsed_value != value:
                return value
            elif isinstance(parsed_value, (int, float, bool)) and (value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit())):
                return parsed_value
            elif isinstance(parsed_value, list) and value.startswith('[') and value.endswith(']'):
                return parsed_value
            elif isinstance(parsed_value, dict) and value.startswith('{') and value.endswith('}'):
                return parsed_value
            elif isinstance(parsed_value, list) and value.startswith('{') and value.endswith('}'):
                return set(parsed_value)
        except json.JSONDecodeError:
            pass
        if value.isdigit():
            try:
                return int(value)
            except ValueError:
                pass
        if value.count('.') == 1 and value.replace('.', '').isdigit():
            try:
                return float(value)
            except ValueError:
                pass
        return value

    @typed
    def set(env: Env='', value: Any=Nill) -> Nill:
        try:
            if env and value:
                os.environ[env] = value
        except Exception as e:
            raise EnvErr(e)

    @typed
    def typeof(env: Env='') -> TYPE:
        value = env.get(env)
        if value is None:
            return None
        return type(value)

    @typed
    def has_value(env: Env='', value: Any=Nill) -> Bool:
        env_value = env.get(env)
        if env_value == value:
            return True
        return False

@service
class envfile:
    @action
    def __new__(cls, trm=None) -> 'envfile':
        from typed import term

        if trm is not None:
            from typed import require
            require.isterm(trm, File)
            return term(trm, ...)

        from utils.path import File
        current_dir = term(__file__, File).absof().parent()

        from typed.poly import join
        while True:
            envpath = join(current_dir, ".env")
            if envpath in File:
                return term(envpath, ...)

            parent_dir = term(envpath, File).parent()
            if parent_dir == current_dir:
                from utils.err import NotFound
                raise NotFound(message="Env file not found in any parent dir.")
            current_dir = parent_dir

        return term(current_dir, ...)

    @action
    def load(trm) -> 'envfile':
        if not trm:
            envpath = env.dotenv()
            if not envpath:
                envpath = '.env'

        if not path.exists(envpath):
            raise EnvErr(f".env file not found.")
        with open(envpath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                comment_index = line.find('#')
                if comment_index != -1:
                    line = line[:comment_index].strip()
                equals_index = line.find('=')
                if equals_index == -1:
                    continue
                key = line[:equals_index].strip()
                value = line[equals_index + 1:].strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                value = value.replace('\\n', '\n')
                value = value.replace('\\r', '\r')
                value = value.replace('\\t', '\t')
                value = value.replace('\\"', '"')
                value = value.replace("\\'", "'")
                value = value.replace('\\\\', '\\')
                os.environ[key] = value
