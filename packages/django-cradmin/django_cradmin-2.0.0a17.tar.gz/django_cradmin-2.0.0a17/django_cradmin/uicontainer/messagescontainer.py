from . import blocklist


class UnsupportedMessageLevel(Exception):
    """
    Raised by :class:`.AbstractMessageContainerMixin` when an unsupported
    message level is requested.
    """


class AbstractMessageContainerMixin(object):
    """
    Defines the interface for message lists.

    This is an abstract mixin. To use it, you inherit this mixin and
    :class:`django_cradmin.uicontainer.container.AbstractContainerRenderable`
    (or a subclass of it), and override :meth:`.create_message_container`.
    """
    #: Supported message levels for :meth:`~.AbstractMessageContainerMixin.add_message`.
    supported_message_levels = {'warning', 'success', 'info'}

    @property
    def should_render(self):
        return self.get_childcount() > 0

    def validate_message_level(self, level):
        """
        Validate that the provided ``level`` is in :obj:`.supported_message_levels`.

        Raises:
            .UnsupportedMessageLevel: If ``level`` is not in :obj:`.supported_message_levels`.
        """
        if level not in self.supported_message_levels:
            raise UnsupportedMessageLevel('{module}.{classname} does not support message level: {level}'.format(
                module=self.__class__.__module__,
                classname=self.__class__.__name__,
                level=level))

    def create_message_container(self, level, text='', **kwargs):
        """
        Create a message container object.

        The returned object must be a subclass of
        :class:`django_cradmin.uicontainer.container.AbstractContainerRenderable`.

        Args:
            level: One of the message levels in :obj:`.supported_message_levels`.
            text: Message text. This is optional. The only use-case for not including
                the message text is to create a more complex message with
                child containers. In that case, you should add child containers
                via ``kwargs``.
            **kwargs: Kwargs for the message container. This means that you
                can create really complex messages by adding any
                AbstractContainerRenderable subclass as a child of the message container.

        Raise:
            .UnsupportedMessageLevel: If ``level`` is not in :obj:`.supported_message_levels` -
                you must implement this behavior in your subclass by calling
                :meth:`.validate_message_level`.

        Returns:
            The created AbstractContainerRenderable object.
        """
        raise NotImplementedError()

    def add_message(self, **kwargs):
        """
        Add a message.

        Creates the message using :meth:`.create_message_container`,
        and adds the message as a child of this container.

        Args:
            **kwargs:: Kwargs for :meth:`.create_message_container`.
        """
        message_container = self.create_message_container(**kwargs)
        return self.add_child(message_container)

    def add_warning(self, **kwargs):
        """
        Add warning message.

        Args:
            **kwargs: Same as for :meth:`.add_message`, the only
                difference is that the ``level`` kwarg is set.
        """
        kwargs['level'] = 'warning'
        return self.add_message(**kwargs)

    def add_success(self, **kwargs):
        """
        Add success message.

        Args:
            **kwargs: Same as for :meth:`.add_message`, the only
                difference is that the ``level`` kwarg is set.
        """
        kwargs['level'] = 'success'
        return self.add_message(**kwargs)

    def add_info(self, **kwargs):
        """
        Add info message.

        Args:
            **kwargs: Same as for :meth:`.add_message`, the only
                difference is that the ``level`` kwarg is set.
        """
        kwargs['level'] = 'info'
        return self.add_message(**kwargs)

    def add_validationerror(self, validationerror, prefix=None, **kwargs):
        """
        Add a :class:`django.forms.ValidationError`.

        Args:
            validationerror: A :class:`django.forms.ValidationError`
            **kwargs: Same as for :meth:`.add_warning`.
        """
        for message in validationerror.messages:
            if prefix:
                message = '{}: {}'.format(prefix, message)
            self.add_warning(text=message, **kwargs)
        return self

    def add_validationerror_list(self, validationerror_list, **kwargs):
        """
        Add a list of :class:`django.forms.ValidationError` objects.

        Just a shortcut for looping through the list and adding errors
        using :meth:`.add_validationerror`.

        Args:
            validationerror_list: A list of :class:`django.forms.ValidationError` objects.
            **kwargs: Same as for :meth:`.add_validationerror`.
        """
        for validationerror in validationerror_list:
            self.add_validationerror(validationerror=validationerror, **kwargs)
        return self


class MessageContainer(blocklist.BlocklistItem):
    """
    Single message container.

    This is a very thin extension of :class:`django_cradmin.uicontainer.blocklist.BlocklistItem`
    that just adds unit test css classes.
    """
    def __init__(self, level, **kwargs):
        """
        Args:
            level: The message level. See :meth:`.AbstractMessageContainerMixin.create_message_container`.
            **kwargs: Kwargs for :class:`django_cradmin.uicontainer.container.AbstractContainerRenderable`.
        """
        self.level = level
        super(MessageContainer, self).__init__(**kwargs)

    def get_default_bem_variant_list(self):
        """
        Default BEM variant set to the level kwarg for :meth:`.__init__`.

        So this assumes that a variant matching the level exists.
        """
        return [self.level]

    def get_default_test_css_class_suffixes_list(self):
        return super(MessageContainer, self).get_default_test_css_class_suffixes_list() + [
            '{}-message'.format(self.level or 'default')
        ]


class MessagesContainer(AbstractMessageContainerMixin, blocklist.Blocklist):
    """
    Messages container - contains zero or more :class:`.MessageContainer`.

    This is a very thin extension of :class:`django_cradmin.uicontainer.blocklist.Blocklist`
    that:

    - Changes the default variant to :obj:`~django_cradmin.uicontainer.blocklist.Blocklist.VARIANT_TIGHT`.
    - Implements :class:`.AbstractMessageContainerMixin` with
      :class:`.MessageContainer` as the message container.
    """
    def create_message_container(self, level, text='', **kwargs):
        return MessageContainer(level=level, text=text, **kwargs)

    def get_default_bem_variant_list(self):
        return ['tight']
