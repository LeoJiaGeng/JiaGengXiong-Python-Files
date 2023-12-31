from configparser import ConfigParser

class Config():
    def __init__(self, file_name= 'config.ini'):
        self.file_name = file_name
        self.config = ConfigParser()
        self.config.read(self.file_name, encoding="utf-8")

    def save(self):
        """Save the configuration"""
        with open(self.file_name,"w+",encoding="utf-8") as file_obj:
            self.config.write(file_obj)

    def get_config(self, section, option):
        """"Returns the value of option in the section"""
        ret = {"ret_val":True, "data":"", "info":"normal operation"}

        if not self.config.has_option(section, option):
            ret["ret_val"] = False
            ret["info"] = "there is no section or option"
            return ret

        ret["data"] = self.config[section][option]
        return ret
    
    def set_config(self, section, option, value):
        """Set the value in the option of the section, if no the option, to create it """
        ret = {"ret_val":True, "data":"", "info":"normal operation"}

        if not self.config.has_section(section):
            ret["ret_val"] = False
            ret["info"] = "there is no section"
        elif not self.config.has_option(section, option):
            ret["info"] = "there is no option, but create one"

        self.config.set(section, option, value)
        self.save()
        return ret
    
    def add_section(self, section):
        """Add a section to the configuration"""
        ret = {"ret_val":True, "data":"", "info":"normal operation"}
        if self.config.has_section(section):
            ret["ret_val"] = False
            ret["info"] = "there has already this section"
            return ret
        
        self.config.add_section(section)
        self.save()
        return ret

    def remove_section(self, section):
        """Remove a section to the configuration"""
        ret = {"ret_val":True, "data":"", "info":"normal operation"}
        if not self.config.has_section(section):
            ret["ret_val"] = False
            ret["info"] = "there is no section"
            return ret

        self.config.remove_section(section)
        self.save()
        return ret

    def remove_option(self, section, option):
        """Remove a option to the configuration"""
        ret = {"ret_val":True, "data":"", "info":"normal operation"}

        if not self.config.has_option(section, option):
            ret["ret_val"] = False
            ret["info"] = "there is no section or option"
            return ret       
        
        self.config.remove_option(section, option)
        self.save()
        return ret

if __name__ == "__main__":
    config = Config()
    print(config.get_config("input", "suffix"))

                    
